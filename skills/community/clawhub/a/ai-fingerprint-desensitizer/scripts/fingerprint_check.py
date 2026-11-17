#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""五维 AI 指纹检测（纯标准库，零依赖，本地跑，内容不出本机）

用法:
    python fingerprint_check.py 文稿.md                 # 单文件检测
    python fingerprint_check.py 原稿.md --compare 改后.md  # 前后对比
    python fingerprint_check.py 文稿.md --top 8           # 列出最像 AI 的 8 句

输出：五个维度得分（0-100，越高越像 AI）+ 综合分 + 命中句定位 + 改进方向
"""
import sys, os, re, math, json, argparse

# ---------- 词表（可自行扩充） ----------
AI_CONNECTORS = ["因此", "然而", "此外", "总之", "综上", "首先", "其次", "最后", "同时",
                 "另外", "值得注意的是", "需要指出的是", "总的来说", "总而言之", "换言之",
                 "与此同时", "在此基础上", "进一步来说", "由此可见", "不仅", "而且"]
AI_PHRASES = ["赋能", "闭环", "抓手", "打法", "心智", "链路", "生态位", "颗粒度", "对齐",
              "拉通", "沉淀", "价值主张", "全链路", "数字化转型", "顶层设计", "多维",
              "深度融合", "全面提升", "有效提升", "极大", "显著", "至关重要", "不可或缺"]
AI_HEDGES = ["在一定程度上", "从某种意义上", "可以说", "某种程度上", "严格来说",
             "需要强调的是", "毋庸置疑", "不可否认", "显而易见"]
FOUR_CHAR = re.compile(r"[\u4e00-\u9fa5]{4}(?=[，。、；：])")
# 只统计"AI 式口号四字词"，不把普通四字词算进去
FOUR_AI = ["深度融合", "全面提升", "有效提升", "持续优化", "不断发展", "深刻变革",
           "广泛关注", "积极推动", "不断加强", "日益增长", "显著提升", "全面深化",
           "深入实施", "扎实推进", "切实有效", "统筹兼顾", "协调推进", "不断完善",
           "持续提升", "有效解决", "充分发挥", "积极探索", "高度关注", "重要支撑"]


def split_sentences(text):
    parts = re.split(r"(?<=[。！？!?；;\n])", text)
    return [p.strip() for p in parts if len(p.strip()) >= 4]


def paragraphs(text):
    return [p.strip() for p in re.split(r"\n\s*\n", text) if p.strip()]


def score_dim(text):
    sents = split_sentences(text)
    paras = paragraphs(text)
    n_char = len(re.sub(r"\s", "", text)) or 1
    res = {}

    # 1) 句式指纹：句长方差 + 关联词密度
    lens = [len(s) for s in sents] or [0]
    mean = sum(lens) / len(lens)
    var = sum((x - mean) ** 2 for x in lens) / len(lens)
    std = math.sqrt(var)
    cv = std / mean if mean else 0                      # 变异系数：越小越均匀
    conn = sum(text.count(c) for c in AI_CONNECTORS)
    conn_rate = conn / (len(sents) or 1)                # 每句关联词数
    hedge = sum(text.count(h) for h in AI_HEDGES)
    s1 = min(100, max(0, (0.45 - cv) / 0.45 * 70 + min(conn_rate, 0.5) / 0.5 * 30))
    res["句式指纹"] = round(s1, 1)
    res["_cv"] = round(cv, 3)
    res["_conn_rate"] = round(conn_rate, 3)
    res["_hedge"] = hedge

    # 2) 词汇指纹：AI 高频词 + AI 式四字口号（按千字归一，短文用 0.5 兜底避免虚高）
    ph = sum(text.count(w) for w in AI_PHRASES)
    four = sum(text.count(w) for w in FOUR_AI)
    denom = max(n_char / 1000, 0.5)
    per_k = (ph * 1.5 + four) / denom
    s2 = min(100, per_k / 22 * 100)
    res["词汇指纹"] = round(s2, 1)
    res["_ai_words"] = ph
    res["_four_char"] = four

    # 3) 结构指纹：段落长度均匀度 + 段首论断率 + 排比
    plens = [len(p) for p in paras] or [0]
    pmean = sum(plens) / len(plens)
    pstd = math.sqrt(sum((x - pmean) ** 2 for x in plens) / len(plens))
    pcv = pstd / pmean if pmean else 0
    heads = [p[:20] for p in paras]
    parallel = sum(1 for h in heads if re.match(r"^[一二三四五六七八九十]、|^第[一二三四五六七八九十]", h))
    bullet = sum(1 for p in paras if re.match(r"^\s*[-*•]|^\s*\d+[.、)]", p))
    s3 = min(100, max(0, (0.5 - pcv) / 0.5 * 50 + parallel / max(len(paras), 1) * 30 + bullet / max(len(paras), 1) * 20))
    res["结构指纹"] = round(s3, 1)
    res["_para_cv"] = round(pcv, 3)

    # 4) 节奏指纹：口语标记、破折号、括号插入、第一人称
    colloquial = len(re.findall(r"其实|说白了|老实说|说实话|我觉着|你会发现|说真的|讲真|扯远了|题外话", text))
    first_person = len(re.findall(r"我|我们|咱们|自己", text))
    dashes = text.count("——") + text.count("–")
    parens = text.count("（") + text.count("(")
    s4 = min(100, max(0, 100 - (colloquial * 12 + min(dashes, 8) * 4 + min(parens, 12) * 3) - min(first_person / max(len(sents), 1) * 40, 30)))
    res["节奏指纹"] = round(s4, 1)
    res["_colloquial"] = colloquial
    res["_first_person"] = first_person

    # 5) 标点指纹：规范度过高（全角统一、无口语标点、无错字痕迹）
    halfwidth = len(re.findall(r"[,.;:!?]", text))
    fullwidth = len(re.findall(r"[，。；：！？]", text))
    mix_ratio = halfwidth / (halfwidth + fullwidth) if (halfwidth + fullwidth) else 0
    ellipsis = text.count("……") + text.count("...")
    exclaim = text.count("！") + text.count("!")
    s5 = min(100, max(0, 100 - min(mix_ratio * 40, 30) - min(ellipsis, 5) * 5 - min(exclaim, 6) * 4))
    res["标点指纹"] = round(s5, 1)
    res["_mix"] = round(mix_ratio, 3)

    total = (s1 * 0.28 + s2 * 0.22 + s3 * 0.2 + s4 * 0.2 + s5 * 0.1)
    res["综合AI味"] = round(total, 1)
    return res


def suspicious_sentences(text, top=6):
    sents = split_sentences(text)
    scored = []
    for s in sents:
        sc = 0
        for c in AI_CONNECTORS:
            if c in s:
                sc += 3
        for w in AI_PHRASES:
            if w in s and "\ufffd" not in w:
                sc += 3
        for h in AI_HEDGES:
            if h in s:
                sc += 2
        sc += len(FOUR_CHAR.findall(s)) * 1.5
        if re.match(r"^[一二三四五六七八九十]、|^第[一二三四五六七八九十]", s):
            sc += 2
        if 40 <= len(s) <= 80:
            sc += 1.5                      # 典型"AI 句长"
        if sc > 0:
            scored.append((round(sc, 1), s[:110]))
    scored.sort(key=lambda x: -x[0])
    return scored[:top]


def verdict(score):
    if score >= 70:
        return "高度像 AI，建议大改（补信息增量，不只是换词）"
    if score >= 50:
        return "偏 AI，建议按最弱维度改写 1-2 轮"
    if score >= 35:
        return "轻微 AI 味，局部调整即可"
    return "人味充足，可以发"


def report(path, top=6):
    text = open(path, encoding="utf-8", errors="ignore").read()
    r = score_dim(text)
    print(f"\n===== 五维 AI 指纹报告：{os.path.basename(path)} =====")
    print(f"字数：{len(re.sub(r'\\s','',text))}")
    dims = ["句式指纹", "词汇指纹", "结构指纹", "节奏指纹", "标点指纹"]
    print("\n维度得分（0-100，越高越像 AI）")
    for d in dims:
        bar = "█" * int(r[d] / 5) + "·" * (20 - int(r[d] / 5))
        print(f"  {d}  {bar}  {r[d]:>5}")
    print(f"\n  综合 AI 味：{r['综合AI味']}   → {verdict(r['综合AI味'])}")
    print(f"\n  诊断细节：句长变异系数={r['_cv']}（<0.45 偏均匀）| 每句关联词={r['_conn_rate']} "
          f"| AI高频词={r['_ai_words']} | 四字词={r['_four_char']} | 口语标记={r['_colloquial']} | 第一人称={r['_first_person']}")
    worst = max(dims, key=lambda d: r[d])
    tips = {
        "句式指纹": "打散句长：刻意插几个 5-10 字短句，减掉'因此/然而/总之'这类关联词",
        "词汇指纹": "删掉'赋能/闭环/抓手'这类词，四字词连用拆开说人话",
        "结构指纹": "别每段都首句论断；把总-分-总改成从一件具体的事讲起",
        "节奏指纹": "加口语插入（'说白了''其实'）、加个人视角（'我遇到的''去年那个项目'）",
        "标点指纹": "允许少量不规范：口语标点、破折号、省略号，别全文一丝不苟",
    }
    print(f"\n  ⚠ 最弱维度：{worst} → {tips[worst]}")
    print("\n最像 AI 的句子（优先改这些）")
    for sc, s in suspicious_sentences(text, top):
        print(f"  [{sc:>4}] {s}")
    print()
    return r


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("path")
    ap.add_argument("--compare", help="改写后的文件，做前后对比")
    ap.add_argument("--top", type=int, default=6)
    a = ap.parse_args()
    r1 = report(a.path, a.top)
    if a.compare:
        r2 = report(a.compare, a.top)
        print("===== 前后对比 =====")
        for d in ["句式指纹", "词汇指纹", "结构指纹", "节奏指纹", "标点指纹", "综合AI味"]:
            delta = r2[d] - r1[d]
            arrow = "↓" if delta < 0 else ("↑" if delta > 0 else "=")
            print(f"  {d:<8} {r1[d]:>5} → {r2[d]:>5}  {arrow}{abs(delta)}")
        print(f"\n结论：{'✅ 改善明显' if r2['综合AI味'] < r1['综合AI味'] - 8 else '⚠ 改善有限，建议按最弱维度再改一轮'}")
