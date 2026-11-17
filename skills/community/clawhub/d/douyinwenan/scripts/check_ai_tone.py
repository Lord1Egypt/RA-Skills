# -*- coding: utf-8 -*-
"""AI 味检测脚本 — 词汇 + 结构 + 连接词密度三维检测

用法:
  python check_ai_tone.py "文案文本"
  python check_ai_tone.py --file draft.txt
  python check_ai_tone.py --json "文案文本"   # 输出 JSON 便于 quality_gate 调用

返回 0-100 分，>=85 通过，70-84 警告，<70 失败。
"""
import argparse
import json
import re
import sys

# 书面总结词（AI 腔重灾区）
AI_SMELL_WORDS = [
    "总而言之", "综上所述", "由此可见", "值得关注", "致力于", "关键在于",
    "赋能", "维度", "抓手", "闭环", "底层逻辑", "颗粒度", "深耕",
    "不仅...更是", "一方面...另一方面", "众所周知", "毋庸置疑",
    "让我们来看看", "接下来我们", "首先...其次...最后", "综上所述",
]

# 官方腔/宣传腔
OFFICIAL_TONE_WORDS = [
    "深入贯彻落实", "扎实推进", "高度重视", "切实", "着力", "进一步",
    "不断提升", "持续优化", "全面加强", "积极推动",
]

# 排比检测：连续 3 个以上相同开头的短句
PARALLEL_RE = re.compile(r"([^，。！？\n]{2,8}[，])\1{2,}")

# 总-分-总 结构词
TOTAL_WORDS = ["总的来说", "总结一下", "最后我想说", "以上就是"]


def check_vocab(text):
    hits = []
    for w in AI_SMELL_WORDS:
        if w in text:
            hits.append(w)
    for w in OFFICIAL_TONE_WORDS:
        if w in text:
            hits.append(w)
    return hits


def check_structure(text):
    """检测排比句、总分总、破折号滥用等 AI 结构特征"""
    issues = []
    if PARALLEL_RE.search(text):
        issues.append("检测到排比句（连续相同开头短句）")
    if any(w in text for w in TOTAL_WORDS):
        issues.append("检测到总-分-总结构词")
    # 破折号滥用（AI 常用 —— 做解释）
    if text.count("——") >= 3:
        issues.append("破折号使用超过 3 次（AI 解释腔）")
    # 冒号滥用
    if text.count("：") >= 6:
        issues.append("冒号使用超过 6 次（列表腔）")
    return issues


def check_connector_density(text):
    """连接词密度：AI 倾向用大量逻辑连接词"""
    connectors = ["因此", "所以", "但是", "然而", "因为", "由于", "同时", "此外",
                  "并且", "而且", "也就是说", "换句话说", "值得注意的是"]
    count = sum(text.count(c) for c in connectors)
    # 粗略按 100 字一个连接词为基线
    length = len(text)
    density = count / max(length / 100, 1)
    return density, count


def score_text(text):
    vocab_hits = check_vocab(text)
    struct_issues = check_structure(text)
    density, conn_count = check_connector_density(text)

    score = 100
    score -= len(vocab_hits) * 8
    score -= len(struct_issues) * 10
    if density > 3.0:
        score -= 10
    elif density > 2.0:
        score -= 5
    score = max(0, min(100, score))
    return score, {
        "vocab_hits": vocab_hits,
        "structure_issues": struct_issues,
        "connector_count": conn_count,
        "connector_density": round(density, 2),
    }


def main():
    parser = argparse.ArgumentParser(description="AI 味检测")
    parser.add_argument("text", nargs="?", help="文案文本")
    parser.add_argument("--file", help="从文件读取")
    parser.add_argument("--json", action="store_true", help="输出 JSON")
    args = parser.parse_args()

    if args.file:
        with open(args.file, encoding="utf-8") as f:
            text = f.read()
    elif args.text:
        text = args.text
    else:
        print("用法: python check_ai_tone.py '文案' 或 --file draft.txt")
        sys.exit(1)

    score, detail = score_text(text)
    if args.json:
        print(json.dumps({"score": score, **detail}, ensure_ascii=False, indent=2))
        return

    print("--- 文案人味测评 ---")
    print(f"得分: {score}/100")
    if detail["vocab_hits"]:
        print(f"AI 腔词汇: {', '.join(detail['vocab_hits'])}")
    if detail["structure_issues"]:
        for i in detail["structure_issues"]:
            print(f"结构问题: {i}")
    if detail["connector_count"]:
        print(f"连接词: {detail['connector_count']} 个 (密度 {detail['connector_density']}/百字)")
    if score >= 85:
        print("通过：文案听起来像真人。")
    elif score >= 70:
        print("警告：有 AI 味，建议按命中项改写。")
    else:
        print("失败：AI 味过重，必须重写。")
    sys.exit(0 if score >= 85 else 1)


if __name__ == "__main__":
    main()
