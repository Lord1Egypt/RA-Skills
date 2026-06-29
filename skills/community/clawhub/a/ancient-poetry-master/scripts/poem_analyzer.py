#!/usr/bin/env python3
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
"""
诗词结构分析器
分析给定诗词的形式特征：体裁识别、押韵检测、平仄分析、字数统计
"""
import re
import sys
import json


# 平水韵常用平声韵部简表
PING_SHENG = {
    "东": "一东", "同": "一东", "铜": "一东", "桐": "一东", "童": "一东",
    "中": "一东", "风": "一东", "空": "一东", "红": "一东", "工": "一东",
    "冬": "二冬", "农": "二冬", "宗": "二冬", "钟": "二冬", "龙": "二冬",
    "松": "二冬", "容": "二冬", "蓉": "二冬", "峰": "二冬", "重": "二冬",
    "江": "三江", "窗": "三江", "双": "三江", "邦": "三江", "降": "三江",
    "时": "四支", "知": "四支", "诗": "四支", "枝": "四支", "期": "四支",
    "思": "四支", "丝": "四支", "池": "四支", "迟": "四支", "离": "四支",
    "归": "五微", "飞": "五微", "衣": "五微", "稀": "五微", "晖": "五微",
    "书": "六鱼", "居": "六鱼", "如": "六鱼", "余": "六鱼", "初": "六鱼",
    "无": "七虞", "湖": "七虞", "孤": "七虞", "途": "七虞", "呼": "七虞",
    "低": "八齐", "西": "八齐", "啼": "八齐", "溪": "八齐", "迷": "八齐",
    "来": "十灰", "开": "十灰", "台": "十灰", "杯": "十灰", "回": "十灰",
    "人": "十一真", "春": "十一真", "尘": "十一真", "新": "十一真", "身": "十一真",
    "门": "十三元", "村": "十三元", "魂": "十三元", "言": "十三元", "园": "十三元",
    "天": "一先", "年": "一先", "前": "一先", "烟": "一先", "边": "一先",
    "然": "一先", "眠": "一先", "田": "一先", "千": "一先", "仙": "一先",
    "遥": "二萧", "桥": "二萧", "消": "二萧", "朝": "二萧", "聊": "二萧",
    "高": "四豪", "涛": "四豪", "劳": "四豪", "毛": "四豪", "骚": "四豪",
    "花": "六麻", "家": "六麻", "华": "六麻", "斜": "六麻", "沙": "六麻",
    "长": "七阳", "光": "七阳", "香": "七阳", "霜": "七阳", "乡": "七阳",
    "阳": "七阳", "凉": "七阳", "伤": "七阳", "忘": "七阳", "茫": "七阳",
    "明": "八庚", "生": "八庚", "声": "八庚", "情": "八庚", "清": "八庚",
    "城": "八庚", "平": "八庚", "惊": "八庚", "鸣": "八庚", "行": "八庚",
    "星": "九青", "青": "九青", "经": "九青", "庭": "九青", "灵": "九青",
    "楼": "十一尤", "秋": "十一尤", "愁": "十一尤", "流": "十一尤", "游": "十一尤",
    "舟": "十一尤", "休": "十一尤", "头": "十一尤", "收": "十一尤", "留": "十一尤",
    "深": "十二侵", "心": "十二侵", "林": "十二侵", "金": "十二侵", "音": "十二侵",
}


def split_lines(poem: str) -> list[str]:
    """按标点拆分诗句"""
    lines = re.split(r'[，,。！？；、\n]', poem)
    return [l.strip() for l in lines if l.strip()]


def detect_form(poem: str) -> dict:
    """检测诗体"""
    lines = split_lines(poem)
    n_lines = len(lines)

    # 计算每句字数
    char_counts = [len(l) for l in lines]
    if not char_counts:
        return {"form": "未知", "detail": "无法解析"}

    avg_chars = sum(char_counts) / len(char_counts)

    form = "古体诗"
    detail = ""

    if n_lines == 4:
        if all(c == 5 for c in char_counts):
            form = "五言绝句"
        elif all(c == 7 for c in char_counts):
            form = "七言绝句"
        else:
            form = "四句古体诗"
    elif n_lines == 8:
        if all(c == 5 for c in char_counts):
            form = "五言律诗"
        elif all(c == 7 for c in char_counts):
            form = "七言律诗"
        else:
            form = "八句古体诗"
    elif all(c == 5 for c in char_counts):
        form = f"五言古诗 ({n_lines}句)"
    elif all(c == 7 for c in char_counts):
        form = f"七言古诗 ({n_lines}句)"
    else:
        form = f"杂言古诗 ({n_lines}句)"

    return {
        "form": form,
        "total_lines": n_lines,
        "chars_per_line": char_counts,
        "total_chars": sum(char_counts),
        "is_regulated": "律" in form or "绝" in form
    }


def detect_rhyme(poem: str) -> dict:
    """检测押韵"""
    lines = split_lines(poem)
    rhyme_chars = []
    rhyme_groups = set()

    # 偶数句最后一个字（近体诗押韵规则）
    for i, line in enumerate(lines):
        if i % 2 == 1 or (len(lines) == 4 and i == 3):  # 偶数句 + 绝句第四句
            if line:
                last_char = line[-1]
                rhyme_chars.append(last_char)
                if last_char in PING_SHENG:
                    rhyme_groups.add(PING_SHENG[last_char])

    is_rhymed = len(rhyme_groups) <= 2 and len(rhyme_chars) >= 2
    rhyme_quality = "完美押韵" if len(rhyme_groups) == 1 else (
        "基本押韵" if len(rhyme_groups) <= 2 else "部分押韵或不押韵"
    )

    return {
        "rhyme_chars": rhyme_chars,
        "rhyme_groups": list(rhyme_groups),
        "is_rhymed": is_rhymed,
        "quality": rhyme_quality
    }


def analyze(poem: str) -> dict:
    """综合分析一首诗"""
    form_result = detect_form(poem)
    rhyme_result = detect_rhyme(poem)

    return {
        "poem": poem.strip(),
        "form": form_result,
        "rhyme": rhyme_result,
        "tags": []
    }


def main():
    if len(sys.argv) > 1:
        poem = sys.argv[1]
    else:
        poem = sys.stdin.read()

    result = analyze(poem)
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
