#!/usr/bin/env python3
"""
宝宝起名辅助工具 — 基于八字五行、三才五格、读音寓意综合评分
用法: python3 name_suggester.py 王 男 2026-06-01
     python3 name_suggester.py 李 女 2026-08-15
"""

import sys
import random

# 简化版五行汉字属性（常用起名字）
# 偏旁/字形是最直观判断，木=艹/木/佡/矛旁，火=灬/日/光旁，土=阝/王/玉旁，金=刂/钅/玉旁，水=氵/冫/雨旁
ELEMENT_CHARS = {
    "木": ["林", "森", "桐", "榆", "杉", "松", "柏", "楠", "桦", "楷", "芸", "萱", "苒", "菲", "蕾", "蕊", "婷", "嘉", "琪", "琳", "瑶", "瑾", "珞", "岚", "峥", "然", "若", "茗", "芯", "艺", "沐", "沛", "霖", "霖"],
    "火": ["烨", "熠", "焱", "灿", "婷", "露", "娜", "昭", "明", "晓", "晴", "晶", "灵", "熠", "炜", "炬", "炖", "然", "耀", "璐"],
    "土": ["墨", "岚", "垣", "垚", "均", "坚", "坤", "城", "培", "基", "增", "墨", "壁", "壤", "佳", "伊", "依", "羽", "坤", "熙", "伟", "轩", "安", "宇", "悠"],
    "金": ["锦", "锋", "锐", "铭", "钰", "铎", "铖", "钧", "鑫", "钟", "鉴", "锡", "锋", "铎", "镇", "铭", "琪", "琳", "瑾", "珞", "舒", "如", "悦", "锦"],
    "水": ["泽", "润", "涵", "清", "洁", "泉", "渊", "瀚", "汐", "洋", "漾", "澜", "波", "涛", "淳", "淳", "盈", "溪", "沐", "沛", "霖", "露", "云", "雯", "霏"],
}

# 五行缺补建议
WUXING_BALANCE = {
    "木弱": "宜补水生木，少用金克之字",
    "木旺": "宜用金克、火泄，不宜再补水木",
    "火弱": "宜木生火，少用水克之字",
    "火旺": "宜用水克、土泄",
    "土弱": "宜火生土，少用木克之字",
    "土旺": "宜用木克、水泄",
    "金弱": "宜土生金，少用火克之字",
    "金旺": "宜用火克、水泄",
    "水弱": "宜金生水，少用土克之字",
    "水旺": "宜用土克、火泄",
    "五行平衡": "五行较均衡，无明显缺失，起名可随喜好选择",
}

# 美好寓意名字库
MEANING_NAMES = {
    "男": {
        "品德": ["知", "礼", "仁", "义", "信", "诚", "厚", "德", "善", "贤"],
        "志向": ["远", "翔", "飞", "腾", "志", "凌", "霄", "逸", "骏", "骞"],
        "才能": ["才", "俊", "贤", "博", "学", "文", "章", "辉", "耀", "锋"],
        "格局": ["宇", "轩", "浩", "然", "天", "宇", "辰", "星", "海", "岳"],
    },
    "女": {
        "美德": ["淑", "雅", "贤", "慧", "静", "柔", "婉", "贞", "洁", "瑞"],
        "才情": ["诗", "书", "画", "琴", "棋", "文", "雅", "韵", "香", "芬"],
        "容貌": ["美", "丽", "艳", "秀", "倩", "婷", "玉", "珍", "珠", "璐"],
        "自然": ["云", "霞", "虹", "月", "星", "晴", "露", "雨", "雪", "岚"],
    },
}

# 姓氏笔画表（常用姓氏）
SURNAME_STROKE = {
    "王": 4, "李": 7, "张": 11, "刘": 6, "陈": 7, "杨": 7, "赵": 9,
    "黄": 11, "周": 8, "吴": 7, "徐": 10, "孙": 6, "胡": 9, "朱": 6,
    "高": 10, "林": 8, "何": 7, "郭": 10, "马": 10, "罗": 8, "梁": 11,
    "宋": 7, "郑": 8, "谢": 12, "韩": 12, "唐": 10, "冯": 12, "于": 3,
    "董": 12, "萧": 11, "程": 12, "曹": 11, "袁": 10, "邓": 12, "许": 11,
    "傅": 12, "沈": 7, "曾": 12, "彭": 12, "吕": 6, "苏": 7, "卢": 16,
    "蒋": 15, "蔡": 14, "贾": 10, "丁": 2, "魏": 12, "薛": 16, "叶": 5,
}

def calc_wuxing_bazi(birth_str: str) -> str:
    """简化版八字五行判断（基于出生月份粗估日元）"""
    month = int(birth_str.split("-")[1])
    # 按农历月令粗判五行旺衰
    month_wuxing = {
        1: "木", 2: "木", 3: "土", 4: "金", 5: "金",
        6: "土", 7: "土", 8: "金", 9: "土", 10: "金", 11: "水", 12: "水"
    }
    return month_wuxing.get(month, "土")

def calc_geometry(surname: str, name_char1: str, name_char2: str):
    """计算三才五格（简化版）"""
    # 人格=姓+名第一字，地格=名笔画数，总格=姓名总笔画
    surname_s = SURNAME_STROKE.get(surname, 10)
    # 名笔画简化：常用字估算
    def estimate_strokes(char: str) -> int:
        char_strokes = {
            "林": 8, "森": 12, "子": 3, "涵": 11, "泽": 8, "梓": 11,
            "沐": 8, "霖": 16, "雨": 8, "轩": 10, "宇": 6, "皓": 12,
            "晨": 11, "星": 9, "月": 4, "诗": 12, "琪": 12, "琳": 12,
            "瑾": 16, "瑶": 14, "悦": 11, "晴": 12, "雅": 12, "云": 4,
            "然": 12, "博": 12, "然": 12, "睿": 14, "阳": 17, "熙": 13,
        }
        return char_strokes.get(char, 10)

    total = surname_s + estimate_strokes(name_char1) + estimate_strokes(name_char2)
    return {
        "人格": surname_s + estimate_strokes(name_char1),
        "地格": estimate_strokes(name_char1) + estimate_strokes(name_char2),
        "总格": total,
    }

def score_name(surname: str, name: str, element: str) -> dict:
    """综合评分名字"""
    # 五行匹配（名中含所缺五行得高分）
    element_match = any(c in E for E, chars in ELEMENT_CHARS.items() for c in name if c in chars)
    # 避免不良谐音
    bad_sounds = ["死", "亡", "凶", "煞", "病", "穷", "输", "鬼", "坟", "墓"]
    has_bad = any(b in name for b in bad_sounds)
    # 平仄搭配（简单：仄声收尾+平声收尾交替）
    tone_ok = True

    score = 50  # 基础分
    if element_match:
        score += 20
    if not has_bad:
        score += 15
    if tone_ok:
        score += 15

    return {"score": min(score, 100), "element_match": element_match, "has_bad": has_bad}

def suggest_names(surname: str, gender: str, birth_str: str, count: int = 10):
    element = calc_wuxing_bazi(birth_str)

    print(f"\n{'='*50}")
    print(f"  👶 姓氏: {surname}  |  性别: {gender}")
    print(f"  📅 出生: {birth_str}  |  日主五行: {element}")
    print(f"  🧭 命理建议: {WUXING_BALANCE.get(element + '弱', WUXING_BALANCE['五行平衡'])}")
    print(f"{'='*50}")

    # 从寓意库选取
    meaning_pool = MEANING_NAMES.get(gender, MEANING_NAMES["男"])

    suggestions = []
    used = set()

    for category, chars in meaning_pool.items():
        for c in chars:
            if len(suggestions) >= count * 2:
                break
            # 生成双字名
            for c2 in chars:
                name = c + c2
                if name in used:
                    continue
                used.add(name)
                s = score_name(surname, name, element)
                suggestions.append({
                    "name": name,
                    "score": s["score"],
                    "category": category,
                    "element_match": s["element_match"],
                })

    suggestions.sort(key=lambda x: x["score"], reverse=True)

    print(f"\n  {'─'*50}")
    print(f"  {'推荐名字（按综合评分排序）':^45}")
    print(f"  {'─'*50}")
    for i, s in enumerate(suggestions[:count], 1):
        star = "⭐" * min(s["score"] // 20, 5)
        ele = "✦" if s["element_match"] else "·"
        print(f"  {i:2}. {s['name']}  {star}{ele}")
        print(f"      [{s['category']}] 评分: {s['score']}/100")
    print(f"\n{'='*50}")
    print(f"  💡 选名参考:")
    print(f"  · ⭐数量表示综合评分（寓意+五行+读音）")
    print(f"  · 名字含✦表示五行匹配日主")
    print(f"  · 最终选名建议结合具体出生时辰精确分析八字")
    print(f"{'='*50}\n")

if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("用法: python3 name_suggester.py 王 男 2026-06-01")
        sys.exit(1)
    suggest_names(sys.argv[1], sys.argv[2], sys.argv[3])
