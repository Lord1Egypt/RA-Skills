#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
按经文查出处.py —— 输入一句经文，自动反查 CBETA 出处并生成完整学术脚注。

与「生成引用.py」的区别：
    生成引用.py   已知出处编号 → 补全出版社/出版年 → 出脚注
    按经文查出处.py 只有一句经文 → 自动定位册/卷/页/栏/行 → 出脚注

原理（全部走 CBETA 官方 API）：
    1. /search      全文检索，确定候选【佛典 + 卷数】
    2. /search/kwic 关键词上下文，取得精确【页码 + 栏 + 行】与原文片段
    3. /works       取得经名、作译者、朝代、册数
    4. 本地 藏经出版社.json 补出版社 / 出版地 / 出版年

用法：
    python 按经文查出处.py "一心三智為妙行本"
    python 按经文查出处.py "一心三智為妙行本" --经 T1717     # 限定佛典，更快更准
    python 按经文查出处.py "一心三智為妙行本" --藏 C          # 只在《中華大藏經》中查
    python 按经文查出处.py "一心三智為妙行本" --中文数字 --复制
"""

import argparse
import importlib.util
import os
import re
import sys
import time
import urllib.parse

目录 = os.path.dirname(os.path.abspath(__file__))
接口根 = "https://cbdata.dila.edu.tw/stable"


# 复用「生成引用.py」的格式化能力，避免重复实现
def 载入主模块():
    路径 = os.path.join(目录, "生成引用.py")
    规格 = importlib.util.spec_from_file_location("生成引用", 路径)
    模块 = importlib.util.module_from_spec(规格)
    规格.loader.exec_module(模块)
    return 模块


主模块 = 载入主模块()
取接口 = 主模块.取接口
载入藏经数据 = 主模块.载入藏经数据
作译者格式 = 主模块.作译者格式
中文数字 = 主模块.中文数字
出版段 = 主模块.出版段
藏经英文名 = 主模块.藏经英文名

标点 = "，。；：、？！「」『』《》（）()〈〉〔〕　 \t\n.\",'‘’“”:;?!-"


def 清理(文本):
    return re.sub("[%s]" % re.escape(标点), "", 文本 or "")


def 取佛典按编号(编号):
    """直接用 work 编号查询（不经补零），兼容 JB348、X0980、T1717 等写法。"""
    数据 = 取接口("/works?work=%s" % urllib.parse.quote(编号))
    结果 = 数据.get("results") or []
    return 结果[0] if 结果 else None


def 全文检索(关键词, 藏=None, 上限=20):
    """/search 返回候选佛典（含卷数），不含页码。"""
    路径 = "/search?q=%s&rows=%d" % (urllib.parse.quote(关键词), 上限)
    if 藏:
        路径 += "&canon=%s" % urllib.parse.quote(藏)
    数据 = 取接口(路径)
    return 数据.get("results") or []


def 取上下文(经号, 卷, 关键词):
    """/search/kwic 返回该卷中命中词的【页码栏行 lb】与原文片段。"""
    数据 = 取接口("/search/kwic?work=%s&juan=%s&q=%s"
                  % (urllib.parse.quote(经号), 卷, urllib.parse.quote(关键词)))
    return 数据.get("results") or []


def 逐步缩短(经文, 藏=None, 经=None):
    """整句常因标点/跨行检索不到，故由长到短自动截取关键词重试。"""
    净 = 清理(经文)
    长度表 = []
    for L in (14, 12, 10, 8, 6, 5, 4):
        if L <= len(净) and L not in 长度表:
            长度表.append(L)
    if len(净) < 4:
        长度表 = [len(净)] if 净 else []
    for L in 长度表:
        词 = 净[:L]
        候选 = 全文检索(词, 藏=藏)
        if 经:
            候选 = [c for c in 候选 if c.get("work") == 经] or 候选
        if 候选:
            return 词, 候选
    return None, []


def 生成脚注(定位, 佛典, 藏经数据, 引文, 详细=True, 用中文数字=False):
    """复用主模块的六种格式生成。"""
    结果 = 主模块.生成全部(定位, 佛典, 藏经数据, 引文,
                    详细=详细, 用中文数字=用中文数字)
    return 结果


def 主程序():
    解析 = argparse.ArgumentParser(
        description="输入一句经文，自动反查 CBETA 出处并生成完整学术脚注。")
    解析.add_argument("经文", help="要查的经文句子，如「一心三智為妙行本」")
    解析.add_argument("--经", default="", help="限定佛典编号，如 T1717（更快更准）")
    解析.add_argument("--藏", default="", help="限定藏经代码，如 C（中華大藏經）、P、F、ZW")
    解析.add_argument("--版本", default="", help="CBETA 版本号，默认 2026.R1")
    解析.add_argument("--最多", type=int, default=5, help="最多显示几笔，默认 5")
    解析.add_argument("--中文数字", dest="用中文数字", action="store_true",
                      help="卷数用中文数字（卷八）")
    解析.add_argument("--简", action="store_true", help="页码用学界简写")
    解析.add_argument("--复制", action="store_true", help="复制第一笔的完整脚注到剪贴板")
    参数 = 解析.parse_args()

    藏经数据 = 载入藏经数据()
    版本 = 参数.版本 or 主模块.默认版本

    词, 候选 = 逐步缩短(参数.经文, 藏=参数.藏 or None, 经=参数.经 or None)
    if not 候选:
        print("【未命中】CBETA 中检索不到「%s」。" % 参数.经文, file=sys.stderr)
        print("建议：① 换用该句中较独特的 4-6 字；② 确认用字与 CBETA 一致（繁体、正字）；"
              "③ 用 --经 指定佛典编号。", file=sys.stderr)
        sys.exit(1)

    print("=" * 68)
    print("检索词：%s    候选佛典：%d 部" % (词, len(候选)))
    print("=" * 68)

    # 若指定了佛典但全文检索未命中，则直接遍历该经各卷，确保「限定」语义成立
    if 参数.经:
        m0 = re.match(r"^([A-Z]{1,2})(\d+[A-Za-z]?)$", 参数.经)
        已选 = [c for c in 候选 if c.get("work") == 参数.经]
        if not 已选:
            佛典0 = 取佛典按编号(参数.经)  # 直接用原编号查，避免 JB348 被补零成 JB0348
            if 佛典0:
                总卷 = int(佛典0.get("juan") or 1)
                已选 = [{"work": 参数.经, "juan": j, "vol": 佛典0.get("vol")}
                        for j in range(1, min(总卷, 80) + 1)]
                print("（全文检索未命中该经，改遍历 %s 全 %d 卷）" % (参数.经, 总卷))
        候选 = 已选 or 候选

    净句 = 清理(参数.经文)
    命中 = []
    for 项 in 候选[:参数.最多 * 3]:
        经号 = 项.get("work")
        卷 = 项.get("juan")
        if not 经号 or not 卷:
            continue
        上下文 = 取上下文(经号, 卷, 词)
        for c in 上下文:
            片段 = c.get("kwic") or ""
            # 优先保留包含整句的命中
            权重 = 2 if (净句 and 清理(片段) and 净句 in 清理(片段)) else (
                1 if 词 in (片段 or "") else 0)
            命中.append({
                "work": 经号, "juan": 卷, "lb": c.get("lb"),
                "vol": c.get("vol") or 项.get("vol"),
                "kwic": 片段, "权重": 权重,
            })
        if len(命中) >= 参数.最多 * 6:
            break
        time.sleep(0.15)  # 轻微限速，避免触发 API 限流

    命中.sort(key=lambda x: -x["权重"])
    命中 = 命中[:参数.最多]

    if not 命中:
        print("【提示】检索到佛典，但该卷内未定位到页码行号，请换更短或更独特的词。")
        sys.exit(1)

    首脚注 = ""
    for 序, h in enumerate(命中, 1):
        # work 形如 T1717 / C1710 / X0980 / JB348 等
        # 以 API 返回的 canon 为准拆出藏经代码，避免把 JB348 误拆成 JB+348
        佛典 = 取佛典按编号(h["work"])
        if not 佛典:
            continue
        藏经 = 佛典.get("canon") or (re.match(r"^[A-Z]{1,2}", h["work"]).group(0)
                                 if re.match(r"^[A-Z]{1,2}", h["work"]) else "T")
        经号 = h["work"][len(藏经):] if h["work"].startswith(藏经) else h["work"]
        册原 = (h.get("vol") or 佛典.get("vol") or "").split("..")[0]
        册 = 主模块.去前导零(re.sub(r"\D", "", 册原))
        lb = h["lb"] or ""
        m2 = re.match(r"^(\d{3,4})([a-z])(\d{2})$", lb)
        if m2:
            页 = 主模块.去前导零(m2.group(1))
            栏 = m2.group(2)
            行 = 主模块.去前导零(m2.group(3))
        else:
            页, 栏, 行 = "", "a", ""
        # 引文优先采用用户输入的原句（若确在该片段内），否则退回 KWIC 上下文
        引文 = 参数.经文 if (净句 and 净句 in 清理(h["kwic"])) else h["kwic"]
        定位 = {
            "藏经": 藏经, "册": 册, "经号": 经号,
            "页": 页, "栏": 栏, "行起": 行, "行止": 行,
            "栏止": 栏, "页止": 页, "版本": 版本, "卷": h["juan"],
        }
        藏数据 = 藏经数据.get(藏经) or 藏经数据.get(藏经[:1]) or {}
        结果 = 生成脚注(定位, 佛典, 藏数据, 引文,
                   详细=not 参数.简, 用中文数字=参数.用中文数字)
        if 序 == 1:
            首脚注 = 结果["完整脚注"]

        print("\n【第 %d 笔】%s  卷%s  %s" % (
            序, 佛典.get("title", ""), h["juan"],
            ("★ 含整句" if h["权重"] == 2 else "○ 含关键词")))
        print("  行首资讯：%s%sn%s_p%s" % (藏经, 册.zfill(2), 经号.zfill(4), lb))
        print("  原文片段：%s" % h["kwic"])
        print("  ① 完整脚注：")
        print("     %s" % 结果["完整脚注"])
        print("  ② 纸本脚注：")
        print("     %s" % 结果["纸本脚注"])
        print("  ④ CBETA 格式：")
        print("     %s" % 结果["CBETA格式"])

    核对网址 = "https://cbetaonline.dila.edu.tw/%s_%s" % (
        命中[0]["work"], str(int(命中[0]["juan"])).zfill(3))
    print("\n" + "=" * 68)
    print("核对网址：%s" % 核对网址)
    print("=" * 68)

    if 参数.复制 and 首脚注:
        try:
            import subprocess
            subprocess.run(["clip"], input=首脚注.encode("utf-16"), check=True)
            print("已复制第一笔「完整脚注」到剪贴板。")
        except Exception as e:
            print("【提示】复制失败（%s），请手动选中复制。" % e, file=sys.stderr)


if __name__ == "__main__":
    主程序()
