#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
更新藏经数据.py

从 CBETA 官方「藏經代碼」页面抓取各藏经的纸本出版信息
（编者 / 出版地 / 出版社 / 出版年），生成 藏经出版社.json 数据表。

来源：https://cbeta.org/collection-notation （CBETA 官方权威资料）

用法：
    python 更新藏经数据.py
"""

import json
import os
import re
import ssl
import subprocess
import sys
import urllib.request
from html import unescape

源网址 = "https://cbeta.org/collection-notation"
输出文件 = os.path.join(os.path.dirname(os.path.abspath(__file__)), "藏经出版社.json")

# 部分藏经的「原版」出版信息（学界通用引用，CBETA 官方引用格式说明所载）
# 说明：CBETA 电子版所据纸本多为重印本，而学术论文通常引用原版，故两者并列。
原版补充 = {
    "T": {
        "原版编者": "大正新脩大藏經刊行會",
        "原版出版地": "東京",
        "原版出版社": "大藏經刊行會",
        "原版出版年": "1924-1935",
        "备注": "学界通用引用为原版（1924-1935）；CBETA 电子版所据为 1988-1991 年普及版。",
    },
    "X": {
        "原版编者": "河村照孝",
        "原版出版地": "東京",
        "原版出版社": "株式會社國書刊行會",
        "原版出版年": "1975-1989",
        "备注": "《卍新纂大日本續藏經》原版与 CBETA 所据一致。",
    },
    "Z": {
        "原版编者": "",
        "原版出版地": "京都",
        "原版出版社": "藏經書院",
        "原版出版年": "1905-1912",
        "备注": "《卍大日本續藏經》原版。",
    },
    "R": {
        "原版编者": "",
        "原版出版地": "台北",
        "原版出版社": "新文豐",
        "原版出版年": "1975",
        "备注": "《卍續藏經．新文豐影印本》。",
    },
}


def 取网页(网址: str) -> str:
    """抓取网页，优先 urllib，证书异常时回退 curl。"""
    try:
        请求 = urllib.request.Request(网址, headers={"User-Agent": "Mozilla/5.0"})
        return urllib.request.urlopen(请求, timeout=30).read().decode("utf-8", "ignore")
    except Exception:
        try:
            结果 = subprocess.run(
                ["curl", "-sL", "-m", "30", "-A", "Mozilla/5.0", 网址],
                capture_output=True,
            )
            return 结果.stdout.decode("utf-8", "ignore")
        except Exception as e:
            print("抓取失败：%s" % e, file=sys.stderr)
            sys.exit(1)


def 解析纸本信息(原文: str):
    """从纸本信息字符串拆出 编者 / 出版地 / 出版社 / 出版年。"""
    文本 = re.sub(r"\s+", " ", unescape(原文 or "")).strip()
    编者 = ""
    剩余 = 文本
    if "／" in 文本:
        段 = 文本.split("／")
        for 项 in 段[:-1]:
            if re.search(r"編|輯|著|譯", 项):
                编者 = 项.strip()
                剩余 = 段[-1]
                break
    出版地 = 出版社 = 出版年 = ""
    # 从后往前逐段尝试，避免把「原刊地」误当出版地（如 R 藏「京都…原刊／台北：新文豐」）
    年份串 = 剩余
    for 段 in reversed(剩余.split("／")):
        匹配 = re.search(r"([^：，。]+)：([^，。]+)", 段)
        if 匹配:
            出版地 = 匹配.group(1).strip()
            出版社 = 匹配.group(2).strip()
            年份串 = 段
            break
    年份 = re.search(r"(\d{3,4}(?:\s*-\s*\d{2,4})?)", 年份串)
    if 年份:
        出版年 = re.sub(r"\s+", "", 年份.group(1))
    return 编者, 出版地, 出版社, 出版年, 文本


def 清洗典籍名(原文: str) -> str:
    """去掉典籍名末尾的英文并列名，保留中文名。"""
    名 = re.sub(r"\s+", " ", (原文 or "")).strip()
    截断 = re.search(r"\s+[A-Za-z]", 名)
    if 截断:
        中文 = 名[: 截断.start()].strip()
        if 中文 and re.search(r"[\u4e00-\u9fff]", 中文):
            return 中文
    return 名


def 主程序():
    网页 = 取网页(源网址)
    表格行 = re.findall(r"<tr[^>]*>(.*?)</tr>", 网页, re.S)
    数据 = {}
    for 行 in 表格行:
        单元格 = re.findall(r"<t[dh][^>]*>(.*?)</t[dh]>", 行, re.S)
        if len(单元格) < 5:
            continue
        格 = [unescape(re.sub(r"<[^>]+>", "", c)).strip() for c in 单元格]
        代码 = 格[0]
        if not 代码 or len(代码) > 4 or 代码 == "代碼":
            continue
        典籍名 = 清洗典籍名(格[1])
        编者, 出版地, 出版社, 出版年, 原文 = 解析纸本信息(格[4])
        记录 = {
            "典籍名": 典籍名,
            "编者": 编者,
            "出版地": 出版地,
            "出版社": 出版社,
            "出版年": 出版年,
            "纸本信息原文": 原文,
        }
        if 代码 in 原版补充:
            记录.update(原版补充[代码])
        数据[代码] = 记录

    with open(输出文件, "w", encoding="utf-8") as f:
        json.dump(数据, f, ensure_ascii=False, indent=1)
    print("已写入 %s，共 %d 部藏经。" % (输出文件, len(数据)))
    for 代码 in ("T", "X", "Z", "R"):
        if 代码 in 数据:
            d = 数据[代码]
            print(
                "  %s %s | 编者:%s | %s:%s | %s"
                % (代码, d["典籍名"], d["编者"], d["出版地"], d["出版社"], d["出版年"])
            )


if __name__ == "__main__":
    主程序()
