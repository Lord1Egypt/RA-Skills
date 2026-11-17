#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
生成引用.py —— CBETA 学术引用（脚注）生成器

功能：
    输入 CBETA 出处编号，输出可直接粘贴到论文脚注的严谨学术引用格式，
    自动补全 CBETA「引用複製」所缺的：作译者、出版社、出版地、出版年。

支持的输入格式：
    T33n1717_p0869b21                        （行首资讯 linehead）
    T33, no. 1717, p. 869b21-22              （论文常用格式）
    CBETA 2026.R1, T33, no. 1717, p. 869b21  （CBETA 完整格式）
    https://cbetaonline.dila.edu.tw/T1717_008（网页网址，仅取经卷）

用法：
    python 生成引用.py "T33, no. 1717, p. 869b21-22"
    python 生成引用.py "T33n1717_p0869b21" --引文 "若一心三觀為妙行本"
    python 生成引用.py "T33, no. 1717, p. 869b21-22" --复制

数据来源（均为官方权威）：
    佛典元数据：CBETA API  https://cbdata.dila.edu.tw/stable/works
    藏经纸本出版信息：CBETA 官方 https://cbeta.org/collection-notation
"""

import argparse
import json
import os
import re
import subprocess
import sys
import urllib.parse
import urllib.request

接口根 = "https://cbdata.dila.edu.tw/stable"
默认版本 = "2026.R1"
数据目录 = os.path.dirname(os.path.abspath(__file__))

栏位名称 = {"a": "上欄", "b": "中欄", "c": "下欄"}
栏位英文 = {"a": "upper", "b": "middle", "c": "lower"}

# 藏经英文名（英文论文引用时用）
藏经英文名 = {
    "T": "Taishō Shinshū Daizōkyō",
    "TW": "Taishō Shinshū Daizōkyō (Xinwenfeng Reprint)",
    "X": "Manji Shinsan Dainihon Zokuzōkyō",
    "Z": "Manji Dainihon Zokuzōkyō",
    "R": "Manji Zokuzōkyō (Xinwenfeng Reprint)",
    "J": "Jiaxing Canon",
    "K": "Tripiṭaka Koreana",
    "C": "Zhonghua Dazangjing",
    "N": "Chinese Translation of the Pāḷi Tipiṭaka",
    "Y": "Corpus of Venerable Yin Shun's Buddhist Studies",
    "L": "Qianlong Edition of the Canon",
    "P": "Northern Yongle Edition of the Canon",
    "Q": "Qisha Edition of the Canon",
    "F": "Fangshan Shijing",
    "B": "Supplement to the Dazangjing",
    "G": "Fojiao Canon",
    "M": "Manji Daizōkyō",
    "S": "Songzang Yizhen",
    "U": "Southern Hongwu Edition of the Canon",
    "A": "Jin Edition of the Canon",
    "TX": "Collected Works of Master Taixu",
    "LC": "Corpus of Lü Cheng's Buddhist Studies",
}

# 出版社英文对照（英文脚注用）
出版社英文 = {
    "大藏出版株式會社": "Daizō Shuppan Kabushikigaisha",
    "大藏經刊行會": "Taishō Issaikyō Kankōkai",
    "株式會社國書刊行會": "Kokusho Kankōkai",
    "藏經書院": "Zokuzōkyō Shoin",
    "新文豐": "Xinwenfeng",
    "中華書局": "Zhonghua Book Company",
    "線裝書局": "Xianzhuang Shuju",
    "民族出版社": "Minzu Press",
    "正聞出版社": "Zhengwen Press",
    "北京圖書館出版社": "Beijing Library Press",
    "華夏出版社": "Huaxia Publishing House",
    "宗教文化出版社": "Religious Culture Press",
    "甘肅文化出版社": "Gansu Culture Press",
    "廣陵書社": "Guangling Shushe",
}

# 朝代英文对照（英文脚注用）
朝代英文 = {
    "漢": "Han", "後漢": "Later Han", "三國": "Three Kingdoms", "吳": "Wu",
    "魏": "Wei", "晉": "Jin", "西晉": "Western Jin", "東晉": "Eastern Jin",
    "姚秦": "Yao Qin", "前秦": "Former Qin", "北涼": "Northern Liang",
    "劉宋": "Liu Song", "蕭齊": "Xiao Qi", "梁": "Liang", "蕭梁": "Xiao Liang",
    "陳": "Chen", "北魏": "Northern Wei", "北齊": "Northern Qi", "高齊": "Gao Qi",
    "北周": "Northern Zhou", "周": "Zhou", "隋": "Sui", "唐": "Tang",
    "五代": "Five Dynasties", "後唐": "Later Tang", "後周": "Later Zhou",
    "宋": "Song", "遼": "Liao", "金": "Jin", "西夏": "Western Xia",
    "元": "Yuan", "明": "Ming", "清": "Qing", "民國": "Republican",
    "現代": "Modern", "高麗": "Goryeo", "新羅": "Silla",
}

# 出版地英文对照
出版地英文 = {
    "東京": "Tokyo", "京都": "Kyoto", "台北": "Taipei", "北京": "Beijing",
    "上海": "Shanghai", "高雄": "Kaohsiung", "新竹": "Hsinchu",
    "成都": "Chengdu", "蘭州": "Lanzhou", "揚州": "Yangzhou",
}

# 罗马字转写（可选功能：安装 pypinyin 后英文脚注可自动带拼音）
try:
    from pypinyin import lazy_pinyin

    def 罗马字(中文: str) -> str:
        if not 中文:
            return ""
        try:
            return " ".join(w.capitalize() for w in lazy_pinyin(中文))
        except Exception:
            return ""
except Exception:
    def 罗马字(中文: str) -> str:
        return ""


# ---------------------------------------------------------------- 基础工具

def 取接口(路径: str, 重试次数=3):
    """调用 CBETA API，优先 urllib，证书异常时回退 curl；失败自动重试。"""
    import time
    网址 = 接口根 + 路径
    头 = {"Referer": "https://cbetaonline.dila.edu.tw"}
    末错 = None
    for 第 in range(重试次数):
        # 通道一：urllib
        try:
            请求 = urllib.request.Request(网址, headers=头)
            return json.loads(
                urllib.request.urlopen(请求, timeout=25).read().decode("utf-8"))
        except Exception as e:
            末错 = e
        # 通道二：curl
        try:
            结果 = subprocess.run(["curl", "-sL", "-m", "25", "-H",
                                   "Referer: https://cbetaonline.dila.edu.tw", 网址],
                                  capture_output=True)
            文本 = 结果.stdout.decode("utf-8", "ignore").strip()
            if 文本.startswith("{"):
                return json.loads(文本)
        except Exception as e:
            末错 = e
        if 第 < 重试次数 - 1:
            time.sleep(1.2 * (第 + 1))  # 退避重试，避免 API 瞬时抖动导致失败
    print("【错误】无法连接 CBETA API（已重试 %d 次）：%s" % (重试次数, 末错),
          file=sys.stderr)
    print("请检查网络后重试。", file=sys.stderr)
    sys.exit(1)


def 载入藏经数据():
    路径 = os.path.join(数据目录, "藏经出版社.json")
    if not os.path.exists(路径):
        print("【提示】缺少 藏经出版社.json，正在生成…", file=sys.stderr)
        subprocess.run([sys.executable, os.path.join(数据目录, "更新藏经数据.py")])
    with open(路径, encoding="utf-8") as f:
        return json.load(f)


# ---------------------------------------------------------------- 解析输入

def 去前导零(串):
    """0869 -> 869、04 -> 4；非数字原样返回。"""
    if not 串:
        return 串
    try:
        return str(int(串))
    except Exception:
        return 串.lstrip("0") or 串


def 解析引用位置(文本: str):
    """从各种 CBETA 引用写法中解析出定位信息。"""
    原 = 文本.strip()
    s = re.sub(r"\s+", " ", 原)
    版本 = 默认版本
    版本匹配 = re.search(r"CBETA\s*(\d{4})[.\-]?(Q?R?\d?)", s, re.I)
    if 版本匹配:
        版本 = 版本匹配.group(1) + "." + (版本匹配.group(2) or "R1").upper().replace("R", "R", 1)
        if not 版本匹配.group(2):
            版本 = 版本匹配.group(1) + ".R1"

    # 格式一：行首资讯 T33n1717_p0869b21 或 T33n1717_p0869b21-22
    #        （经号兼容嘉兴藏「B348」「J271」等带字母前缀编号，如 J36nB348_p0334a11）
    m = re.search(r"\b([A-Z]{1,2})(\d{2,3})n([0-9A-Za-z]{3,4})_p(\d{4})([a-z])(\d{2})(?:-(\d{2}))?", s)
    if m:
        return {
            "藏经": m.group(1), "册": m.group(2), "经号": m.group(3),
            "页": 去前导零(m.group(4)), "栏": m.group(5),
            "行起": 去前导零(m.group(6)), "行止": 去前导零(m.group(7) or m.group(6)),
            "栏止": m.group(5), "页止": 去前导零(m.group(4)), "版本": 版本,
        }

    # 格式二：论文常用 T33, no. 1717, p. 869b21-22
    m = re.search(
        r"\b([A-Z]{1,2})\s*(\d{1,3})\s*,\s*no\.?\s*([0-9A-Za-z]{3,4})\s*,\s*"
        r"(p{1,2})\.?\s*(\d{1,4})\s*([a-z]?)\s*(\d{1,2})?\s*"
        r"(?:[-~]\s*([a-z]?)\s*(\d{1,2}))?", s, re.I)
    if m:
        行起 = 去前导零(m.group(7) or "")
        行止 = 去前导零(m.group(9) or "") or 行起
        栏止 = m.group(8) or m.group(6) or ""
        return {
            "藏经": m.group(1), "册": m.group(2), "经号": m.group(3),
            "页": 去前导零(m.group(5)), "栏": m.group(6) or "a",
            "行起": 行起, "行止": 行止, "栏止": 栏止,
            "页止": 去前导零(m.group(5)), "版本": 版本,
        }

    # 格式三：CBETA Online 网址 https://cbetaonline.dila.edu.tw/T1717_008
    m = re.search(r"([A-Z]{1,2})(\d{4})_(\d{3})", s)
    if m:
        return {
            "藏经": m.group(1), "册": "", "经号": m.group(2),
            "页": "", "栏": "", "行起": "", "行止": "",
            "栏止": "", "页止": "", "版本": 版本, "仅经卷": m.group(3).lstrip("0") or "1",
        }
    return None


# ---------------------------------------------------------------- 取官方数据

def 取佛典信息(藏经: str, 经号: str):
    # API 要求经号为 4 位（如 X0980），用户输入可能为 980，查询时补零
    查号 = 经号.zfill(4) if 经号.isdigit() else 经号
    编号 = 藏经 + 查号
    数据 = 取接口("/works?work=%s" % urllib.parse.quote(编号))
    结果 = 数据.get("results") or []
    return 结果[0] if 结果 else None


def 取卷数(定位: dict):
    """用 goto 接口确认该行所属卷数。行首资讯须补零：册2位、页4位、行2位。"""
    经号4 = 定位["经号"].zfill(4) if 定位["经号"].isdigit() else 定位["经号"]
    if 定位.get("行起"):
        行首 = "%s%sn%s_p%s%s%s" % (
            定位["藏经"], 定位["册"].zfill(2), 经号4,
            (定位["页"] or "0").zfill(4), 定位["栏"] or "a",
            (定位["行起"] or "01").zfill(2))
    else:
        行首 = "%s%sn%s" % (定位["藏经"], 定位["册"].zfill(2), 经号4)
    数据 = 取接口("/juans/goto?linehead=%s" % urllib.parse.quote(行首))
    结果 = 数据.get("results") or []
    return (结果[0].get("juan") if 结果 else None), 行首


# ---------------------------------------------------------------- 格式化输出

def 中文数字卷(卷):
    return 卷 if 卷 is None else str(int(卷))


def 中文数字(数):
    """阿拉伯数字卷数转中文数字：8→八，20→二十，35→三十五。"""
    表 = "零一二三四五六七八九"
    try:
        n = int(数)
    except Exception:
        return str(数)
    if n < 10:
        return 表[n]
    if n < 20:
        return "十" + (表[n % 10] if n % 10 else "")
    if n < 100:
        return 表[n // 10] + "十" + (表[n % 10] if n % 10 else "")
    return str(n)


def 作译者格式(byline: str):
    """把「唐 湛然述」转成「〔唐〕湛然述」。"""
    if not byline:
        return ""
    m = re.match(r"^([^\s]{1,4})\s+(.+)$", byline.strip())
    if m and re.search(r"[\u4e00-\u9fff]", m.group(1)):
        return "〔%s〕%s" % (m.group(1), m.group(2).strip())
    return byline.strip()


def 页码段(定位: dict, 详细=True):
    """生成「第869頁中欄第21-22行」或「頁869中欄21-22行」。无页码时返回空串。"""
    if not (定位.get("页") or ""):
        return ""
    页 = int(定位["页"])
    栏 = 定位["栏"] or "a"
    栏名 = 栏位名称.get(栏, 栏)
    起, 止 = 定位["行起"], 定位["行止"]
    if 详细:
        if 起 and 止 and 起 != 止:
            return "第%d頁%s第%s-%s行" % (页, 栏名, 起, 止)
        if 起:
            return "第%d頁%s第%s行" % (页, 栏名, 起)
        return "第%d頁%s" % (页, 栏名)
    # 学界简写 869中21-22
    简栏 = {"a": "上", "b": "中", "c": "下"}.get(栏, 栏)
    if 起 and 止 and 起 != 止:
        return "頁%d%s%s-%s" % (页, 简栏, 起, 止)
    if 起:
        return "頁%d%s%s" % (页, 简栏, 起)
    return "頁%d%s" % (页, 简栏)


def CBETA编号段(定位: dict):
    """生成 CBETA 官方引用编号：T33, no. 1717, p. 869b21-22"""
    起 = 定位["行起"]
    止 = 定位["行止"]
    栏止 = 定位.get("栏止") or 定位["栏"]
    尾 = ""
    if 起:
        if 止 and 止 != 起:
            尾 = "%s%s-%s" % (定位["栏"], 起, 止)
        else:
            尾 = "%s%s" % (定位["栏"], 起)
    if not (定位.get("页") or ""):  # 仅有经卷、无页码（如网址输入）
        return "%s%s, no. %s" % (定位["藏经"], 定位["册"], 定位["经号"])
    return "%s%s, no. %s, p. %s%s" % (
        定位["藏经"], 定位["册"], 定位["经号"], 定位["页"], 尾)


def 出版段(藏经数据: dict, 用原版=False):
    """生成「東京：大藏出版株式會社，1988-1991年」"""
    if not 藏经数据:
        return ""
    if 用原版 and 藏经数据.get("原版出版社"):
        地 = 藏经数据.get("原版出版地") or ""
        社 = 藏经数据.get("原版出版社") or ""
        年 = 藏经数据.get("原版出版年") or ""
    else:
        地 = 藏经数据.get("出版地") or ""
        社 = 藏经数据.get("出版社") or ""
        年 = 藏经数据.get("出版年") or ""
    if not 社:
        return ""
    段 = ""
    if 地:
        段 += 地 + "："
    段 += 社
    if 年:
        段 += "，%s年" % 年
    return 段


def 生成全部(定位, 佛典, 藏经数据, 引文="", 详细=True, 用中文数字=False):
    经名 = 佛典.get("title", "")
    卷 = 定位.get("卷")
    卷号 = 定位.get("仅经卷") or 卷
    作译者 = 作译者格式(佛典.get("byline", ""))
    册 = 定位["册"] or re.sub(r"\D", "", 佛典.get("vol", "") or "")
    藏经名 = 藏经数据.get("典籍名", "") if 藏经数据 else ""
    编号 = CBETA编号段(定位)
    出版 = 出版段(藏经数据, 用原版=False)
    出版原版 = 出版段(藏经数据, 用原版=True)
    引文段 = "：「%s」" % 引文 if 引文 else ""
    卷段 = "卷%s" % (中文数字(卷号) if 用中文数字 else 中文数字卷(卷号)) if 卷号 else ""

    结果 = {}

    # 1. 完整学术脚注（纸本出版信息 + CBETA 电子定位）—— 推荐
    页段 = 页码段(定位, 详细)
    首 = (作译者 + "，") if 作译者 else ""
    首 += "《%s》%s%s，收入《%s》第%s冊，第%s號%s" % (
        经名, 卷段, 引文段, 藏经名, 册, 定位["经号"],
        ("，" + 页段) if 页段 else "")
    if 出版:
        首 += "，" + 出版
    首 += "；CBETA %s, %s。" % (定位["版本"], 编号)
    结果["完整脚注"] = 首

    # 2. 传统纸本脚注（用原版出版信息，学术期刊常见）
    纸 = (作译者 + "，") if 作译者 else ""
    纸 += "《%s》%s%s，收入《%s》第%s冊，第%s號%s" % (
        经名, 卷段, 引文段, 藏经名, 册, 定位["经号"],
        ("，" + 页段) if 页段 else "")
    if 出版原版 or 出版:
        纸 += "，" + (出版原版 or 出版)
    纸 += "。"
    结果["纸本脚注"] = 纸

    # 3. CBETA 官方格式
    结果["CBETA格式"] = "《%s》%s%s(CBETA %s, %s)" % (
        经名, 卷段, 引文段, 定位["版本"], 编号)

    # 4. 英文脚注（英文论文引用汉文佛典通行做法：保留中文经名，藏经附英文名）
    英页 = "%s%s%s" % (定位["页"], 定位["栏"], 定位["行起"] or "")
    if 定位["行止"] and 定位["行止"] != 定位["行起"]:
        英页 += "-%s" % 定位["行止"]
    英出 = ""
    if 藏经数据:
        社 = 藏经数据.get("出版社") or ""
        社英 = 出版社英文.get(社, 社)
        地英 = 出版地英文.get(藏经数据.get("出版地", ""), 藏经数据.get("出版地") or "")
        年 = 藏经数据.get("出版年") or ""
        英出 = "%s: %s, %s" % (地英, 社英, 年) if 社 else ""
    英藏经 = 藏经英文名.get(定位["藏经"], 藏经名)
    英经名 = 罗马字(经名)
    英作 = 罗马字(佛典.get("creators", ""))
    朝代英 = 朝代英文.get(佛典.get("time_dynasty", ""), 佛典.get("time_dynasty", ""))
    作者段 = ""
    if 佛典.get("creators"):
        作者段 = ("%s %s" % (英作, 佛典["creators"])) if 英作 else 佛典["creators"]
        if 朝代英:
            作者段 += " (%s)" % 朝代英
    经名段 = ("%s 《%s》" % (英经名, 经名)) if 英经名 else "《%s》" % 经名
    首段 = ("%s, %s" % (作者段, 经名段)) if 作者段 else 经名段
    英页码段 = ("p. " + 英页) if 英页 else ""
    结果["英文脚注"] = "%s, juan %s, in %s, vol. %s, no. %s%s%s CBETA %s." % (
        首段, 中文数字卷(卷号) or "?", 英藏经, 册, 定位["经号"],
        (", " + 英页码段) if 英页码段 else "",
        (" (%s)" % 英出) if 英出 else "", 定位["版本"])

    # 5. 参考文献条目
    书 = "《%s》%s卷" % (经名, 佛典.get("juan", "") or "")
    结果["参考文献"] = "%s%s。收入《%s》第%s冊，第%s號。%s。" % (
        作译者, "，" + 书 if 书 else "", 藏经名, 册, 定位["经号"],
        (出版 or 出版原版))

    # 7. 论文署名声明（CBETA 基金会来源说明，正式论文置于参考文献前）
    结果["署名声明"] = (
        "《%s》的資料引用出自「財團法人佛教電子佛典基金會」"
        "(Comprehensive Buddhist Electronic Text Archive Foundation，"
        "簡稱 CBETA Foundation 或 CBETA 基金會)的電子佛典集成。"
        "其出處依冊數、經號、頁數、欄數、行數之順序紀錄，"
        "例如：CBETA %s, %s。" % (藏经名, 定位["版本"], 编号)
    )

    # 6. 简式（学界最常用简写）
    简页 = 页码段(定位, 详细=False)
    简主体 = "《%s》%s%s，%s" % (
        经名, 卷段, 引文段,
        ("《%s》第%s冊，第%s號" % (藏经名, 册, 定位["经号"])) if 藏经名 else "")
    if 简页:
        简主体 += "，" + 简页
    结果["简式脚注"] = 简主体 + "；CBETA %s, %s。" % (定位["版本"], 编号)

    经号4 = 定位["经号"].zfill(4) if 定位["经号"].isdigit() else 定位["经号"]
    卷级网址 = "https://cbetaonline.dila.edu.tw/zh/%s%s_%s" % (
        定位["藏经"], 经号4, str(int(卷号 or 1)).zfill(3))
    # 行级深链：采用 CBETA Online 官方路径式 linehead 定位（zh/{linehead}），精确到行且稳定可靠。
    # 例：https://cbetaonline.dila.edu.tw/zh/T46n1939_p0938c04 —— 与 CBETA 标准"行首资讯"同源。
    # 仅当已有页/栏/行定位时才用行级深链，否则回退卷级。
    if 定位.get("页") and 定位.get("行起"):
        行首 = "%s%sn%s_p%s%s%s" % (
            定位["藏经"], 定位["册"].zfill(2), 经号4,
            str(定位["页"]).zfill(4), 定位["栏"], str(定位["行起"]).zfill(2))
        结果["核对网址"] = "https://cbetaonline.dila.edu.tw/zh/%s" % 行首
        结果["核对网址卷级"] = 卷级网址
    else:
        结果["核对网址"] = 卷级网址
    return 结果


# ---------------------------------------------------------------- 主程序

# 佛学专名保护表：zhconv 会转成 Unicode 扩展区字（多数字体无字形，显示为豆腐块），
# 这些字学界通行保留原字形，故转简后改回。新增误转字直接往下表加。
专名保护表 = {
    "𫖮": "顗",      # 智顗（天台大师），zhconv 误转为扩展 B 区字
}


def 转简(文本: str) -> str:
    """繁体转简体（需 zhconv；未安装时原样返回，不影响其他输出）。"""
    if not 文本:
        return 文本
    try:
        import zhconv
        结果 = zhconv.convert(文本, "zh-cn")
        for 误, 正 in 专名保护表.items():
            结果 = 结果.replace(误, 正)
        return 结果
    except Exception:
        return 文本


def 主程序():
    解析 = argparse.ArgumentParser(
        description="CBETA 学术引用（脚注）生成器：输入出处编号，输出含出版社/出版年/作译者的完整脚注。")
    解析.add_argument("引用", help="CBETA 出处，如 \"T33, no. 1717, p. 869b21-22\"")
    解析.add_argument("--引文", default="", help="要引用的经文句子（可选，自动填入「」中）")
    解析.add_argument("--版本", default="", help="CBETA 版本号，默认 %s" % 默认版本)
    解析.add_argument("--简", action="store_true", help="页码用学界简写（頁869中21-22）")
    解析.add_argument("--中文数字", dest="用中文数字", action="store_true",
                      help="卷数用中文数字（如「卷八」）")
    解析.add_argument("--json", action="store_true", help="以 JSON 输出")
    解析.add_argument("--复制", action="store_true", help="把「文献条目」复制到系统剪贴板")
    解析.add_argument("--全格式", dest="全格式", action="store_true",
                     help="输出七种脚注（默认只出文献条目＋CBETA 定位两行）")
    解析.add_argument("--繁", dest="繁", action="store_true",
                     help="保留 CBETA 原字形（繁体）；默认为简体")
    解析.add_argument("--详细", dest="详细", action="store_true",
                     help="默认两行之外，附核对网址")
    参数 = 解析.parse_args()

    定位 = 解析引用位置(参数.引用)
    if not 定位:
        print("【错误】无法识别的 CBETA 引用格式：%s" % 参数.引用, file=sys.stderr)
        print("支持示例：", file=sys.stderr)
        print("  T33, no. 1717, p. 869b21-22", file=sys.stderr)
        print("  T33n1717_p0869b21", file=sys.stderr)
        print("  https://cbetaonline.dila.edu.tw/T1717_008", file=sys.stderr)
        sys.exit(1)
    if 参数.版本:
        定位["版本"] = 参数.版本

    佛典 = 取佛典信息(定位["藏经"], 定位["经号"])
    if not 佛典:
        print("【错误】CBETA 查无此佛典：%s%s" % (定位["藏经"], 定位["经号"]), file=sys.stderr)
        sys.exit(1)

    # 册数缺省时用 API 的 vol
    if not 定位["册"]:
        定位["册"] = re.sub(r"\D", "", 佛典.get("vol", "") or "")
    # 确认卷数
    卷, 行首 = 取卷数(定位)
    定位["卷"] = 卷

    藏经数据 = 载入藏经数据().get(定位["藏经"], {})
    结果 = 生成全部(定位, 佛典, 藏经数据, 参数.引文,
                详细=not 参数.简, 用中文数字=参数.用中文数字)

    if 参数.json:
        print(json.dumps(结果, ensure_ascii=False, indent=1))
        return

    if not 参数.繁:
        结果 = {键: 转简(值) if isinstance(值, str) else 值 for 键, 值 in 结果.items()}
        标题 = 转简("《%s》" % 佛典.get("title", ""))
    else:
        标题 = "《%s》" % 佛典.get("title", "")

    # 默认输出：文献条目一行 + CBETA 定位一行（可直接粘贴进脚注）
    引文调 = 转简(参数.引文) if not 参数.繁 else 参数.引文
    引文段 = "：「%s」" % 引文调 if 引文调 else ""
    核心条目 = 结果["完整脚注"]
    if 引文段:
        if 引文段 not in 核心条目:          # 简体化后引号可能由「」转为“”
            引文段 = "：“%s”" % 引文调
        核心条目 = 核心条目.replace(引文段, "")
    核心条目 = 核心条目.replace("，收入《", "，《").split("；CBETA")[0].rstrip("。") + "。"
    定位串 = "CBETA %s, %s%s, no. %s, p. %s%s%s" % (
        结果.get("版本") or 定位.get("版本") or 默认版本,
        定位.get("藏经", ""), 定位.get("册", ""), 定位.get("经号", ""),
        定位.get("页", ""), 定位.get("栏", ""), 定位.get("行起", ""))
    if 定位.get("行止") and 定位.get("行止") != 定位.get("行起"):
        定位串 += "-%s" % 定位.get("行止")
    定位行 = 定位串 + "。"
    复制文本 = 核心条目 + "\n" + 定位行

    if not 参数.全格式:
        print(核心条目)
        print(定位行)
        if 结果.get("核对网址卷级"):
            print("核对（精确到行）：%s" % 结果["核对网址"])
            print("（卷级）%s" % 结果["核对网址卷级"])
        else:
            print("核对：%s" % 结果["核对网址"])
        if 参数.复制:
            try:
                subprocess.run(["clip"], input=复制文本.encode("utf-16"), check=True)
                print("（已复制两行到剪贴板）", file=sys.stderr)
            except Exception as e:
                print("【提示】复制失败（%s），请手动选中复制。" % e, file=sys.stderr)
        return

    print("=" * 66)
    print("CBETA 学术引用生成结果    %s" % 标题)
    print("行首资讯：%s" % 行首)
    print("作译者：%s" % (佛典.get("byline") or "（未著录）"))
    print("=" * 66)
    for 键, 标签 in [("完整脚注", "① 完整学术脚注（推荐，含出版社＋CBETA 定位）"),
                     ("纸本脚注", "② 传统纸本脚注（用原版出版資訊）"),
                     ("简式脚注", "③ 简式脚注（学界常用简写）"),
                     ("CBETA格式", "④ CBETA 官方引用複製格式"),
                     ("英文脚注", "⑤ 英文脚注"),
                     ("参考文献", "⑥ 参考文献条目"),
                     ("署名声明", "⑦ 论文署名声明（CBETA 基金会来源说明）")]:
        print("\n【%s】\n%s" % (标签, 结果[键]))
    if 结果.get("核对网址卷级"):
        print("\n【核对网址（精确到行）】%s" % 结果["核对网址"])
        print("（卷级）%s" % 结果["核对网址卷级"])
    else:
        print("\n【核对网址】%s" % 结果["核对网址"])
    print("=" * 66)

    if 参数.复制:
        try:
            subprocess.run(["clip"], input=核心条目.encode("utf-16"),
                           check=True)
            print("已复制「文献条目」到剪贴板。")
        except Exception as e:
            print("【提示】复制失败（%s），请手动选中复制。" % e, file=sys.stderr)


if __name__ == "__main__":
    主程序()
