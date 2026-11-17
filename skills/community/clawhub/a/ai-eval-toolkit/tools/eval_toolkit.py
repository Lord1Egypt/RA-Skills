# -*- coding: utf-8 -*-
"""LLM 评测工具链 - 可运行评测引擎（零依赖，Python 标准库）

引擎：
  dataset      评测集管理（init 建模板 / check 质量检查 / stat 规模统计）
  hallucination 幻觉检测（数字一致性/引用校验/否定矛盾/关键论断互证）
  ragscore     RAG 指标（RAGAS 四指标本地简化：忠实度/答案相关性/上下文精度/上下文召回）
  compare      回归对比（基线 vs 新结果差异判定）
  report       报告生成 + 上线门禁判定

原则：零依赖、本地闭环、可解释（每条判定给出依据）、召回优先（宁误报不漏报）。
"""
import argparse
import json
import os
import re
import sys

# ================= 评测集管理 =================

DATASET_TEMPLATE = """{"id": "case-001", "scenario": "客服问答", "question": "示例问题？", "answer": "示例回答", "context": "检索上下文（可选）", "reference": "标准答案（可选）", "gold": 1, "type": "normal"}"""

REQUIRED_FIELDS = ["id", "scenario", "question"]


def dataset_init(out):
    if os.path.exists(out):
        print(f"错误：{out} 已存在（不覆盖）。")
        return 2
    with open(out, "w", encoding="utf-8") as f:
        f.write(DATASET_TEMPLATE + "\n")
    print(f"评测集模板已生成：{out}")
    print("字段：id(必填)/scenario(必填)/question(必填)/answer/context/reference/gold/type")
    return 0


def dataset_check(path):
    if not os.path.exists(path):
        print(f"错误：文件不存在 {path}")
        return 2
    errs, warns = [], []
    seen = set()
    n = 0
    with open(path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            n += 1
            try:
                case = json.loads(line)
            except json.JSONDecodeError as e:
                errs.append(f"第 {n} 行 JSON 解析失败：{e}")
                continue
            for field in REQUIRED_FIELDS:
                if not case.get(field):
                    errs.append(f"第 {n} 行缺必填字段：{field}")
            cid = case.get("id")
            if cid in seen:
                errs.append(f"id 重复：{cid}")
            seen.add(cid)
            if not case.get("answer") and not case.get("context"):
                warns.append(f"第 {n} 行 answer 与 context 都为空")
    print(f"检查完成：{n} 条用例")
    for w in warns:
        print(f"  ⚠️ {w}")
    for e in errs:
        print(f"  ❌ {e}")
    if errs:
        print(f"结果：{len(errs)} 错误（需修复）/ {len(warns)} 警告")
        return 1
    print(f"结果：通过（{len(warns)} 警告）")
    return 0


def dataset_stat(path):
    if not os.path.exists(path):
        print(f"错误：文件不存在 {path}")
        return 2
    total = 0
    by_scenario, by_type = {}, {}
    with open(path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                case = json.loads(line)
            except json.JSONDecodeError:
                continue
            total += 1
            by_scenario[case.get("scenario", "未标注")] = by_scenario.get(case.get("scenario", "未标注"), 0) + 1
            by_type[case.get("type", "未标注")] = by_type.get(case.get("type", "未标注"), 0) + 1
    print(f"评测集规模：{total} 条")
    print("分场景：")
    for k, v in sorted(by_scenario.items(), key=lambda x: -x[1]):
        print(f"  {k}: {v}")
    print("分类型：")
    for k, v in sorted(by_type.items(), key=lambda x: -x[1]):
        print(f"  {k}: {v}")
    return 0


# ================= 幻觉检测 =================

def _extract_numbers(text):
    """提取数字（含千分位/百分数/万单位），返回归一化数值列表"""
    nums = []
    for m in re.finditer(r"(\d+(?:[,.]\d+)?)\s*(%|万|亿)?", text):
        raw = m.group(1).replace(",", "")
        try:
            val = float(raw)
        except ValueError:
            continue
        unit = m.group(2) or ""
        if unit == "%":
            val = val  # 百分比单独比较
        elif unit == "万":
            val = val * 10000
        elif unit == "亿":
            val = val * 100000000
        nums.append((val, unit))
    return nums


def check_numeric(answer, source):
    """数字一致性：回答中的数字是否在来源中有对应"""
    hits = []
    for val, unit in _extract_numbers(answer):
        if unit == "%":
            continue  # 百分比不做近似
        if 1900 <= val <= 2100:
            continue  # 年份不判矛盾（合理时间表述）
        found = any(abs(val - sval) < 1e-6 for sval, _ in _extract_numbers(source))
        if not found:
            hits.append(f"回答含数字 {val:g} 在来源中未找到对应值")
    return hits


def check_citation(answer, source):
    """引用校验：引号/书名号内容是否在来源中出现"""
    hits = []
    for m in re.finditer(r"[“\"『]([^”\"』]{2,40})[”\"』]", answer):
        quote = m.group(1)
        if quote not in source:
            hits.append(f"引用「{quote}」在来源中未找到")
    return hits


def check_negation(answer, source):
    """否定矛盾：回答中否定表述与来源冲突"""
    hits = []
    neg_patterns = ["不", "无", "未", "没有", "无法", "并非", "不是", "不含"]
    # 提取来源中的关键短语（2-6 字连续词）
    phrases = set(re.findall(r"[\u4e00-\u9fa5A-Za-z]{2,8}", source))
    for neg in neg_patterns:
        for m in re.finditer(neg + r"([\u4e00-\u9fa5]{2,6})", answer):
            tail = m.group(1)
            for phrase in phrases:
                if tail in phrase or phrase in tail:
                    hits.append(f"回答否定「{neg}{tail}」，来源含「{phrase}」")
                    break
    return hits


def check_keyclaim(answer, source):
    """关键论断互证：回答中的关键词（实体/术语）是否被来源覆盖"""
    hits = []
    # 提取回答中的候选实体/术语（连续中文词 ≥2 字 或 英文词）
    keys = set(re.findall(r"[\u4e00-\u9fa5]{2,8}", answer))
    keys |= set(re.findall(r"[A-Za-z][A-Za-z0-9_-]{2,20}", answer))
    # 过滤常见虚词
    stop = {"以及", "可以", "进行", "通过", "相关", "需要", "这个", "那个", "就是", "一个", "没有", "不是", "无法", "包括", "由于", "因此", "所以", "如果", "但是", "因为", "然后", "例如"}
    missing = [k for k in keys if k not in stop and len(k) >= 2 and k not in source]
    if missing:
        hits.append(f"回答关键信息「{'/'.join(sorted(missing)[:5])}」在来源中未覆盖（可能张冠李戴或编造）")
    return hits


def cmd_hallucination(args):
    if not args.answer:
        print("错误：--answer 必填。")
        return 2
    source = args.source or ""
    rules = [
        ("数字一致性", check_numeric(args.answer, source)),
        ("引用校验", check_citation(args.answer, source)),
        ("否定矛盾", check_negation(args.answer, source)),
        ("关键论断互证", check_keyclaim(args.answer, source)),
    ]
    hits = [(name, d) for name, details in rules for d in details]
    print("=" * 60)
    print("幻觉检测结果：")
    if not hits:
        print("  ✅ 未命中规则（clean）——注意：规则覆盖有限，无来源对比时检不出编造")
        return 0
    print(f"  ⚠️ 命中 {len(hits)} 条（suspicious，需人工复核）：")
    for name, detail in hits[:10]:
        print(f"    [{name}] {detail}")
    return 0


# ================= RAG 指标（词重叠简化） =================

def _tokens(text):
    """分词：中文 2-gram + 英文词"""
    tokens = set()
    for m in re.finditer(r"[\u4e00-\u9fa5]", text):
        pass
    cn = re.findall(r"[\u4e00-\u9fa5]+", text)
    for seg in cn:
        if len(seg) == 1:
            tokens.add(seg)
        else:
            for i in range(len(seg) - 1):
                tokens.add(seg[i:i + 2])
    tokens |= set(re.findall(r"[A-Za-z0-9][A-Za-z0-9_-]{1,20}", text))
    return tokens


def _overlap(a, b):
    if not a or not b:
        return 0.0
    return len(a & b) / len(b)


def cmd_ragscore(args):
    q = args.question or ""
    a = args.answer or ""
    c = args.context or ""
    if not a:
        print("错误：--answer 必填。")
        return 2
    tq, ta, tc = _tokens(q), _tokens(a), _tokens(c)
    faith = _overlap(ta, ta & tc) if tc else 0.0
    # 忠实度：回答 Token 中被上下文覆盖的比例
    faith = len(ta & tc) / len(ta) if ta else 0.0
    relevance = _overlap(ta, tq)
    # 上下文精度：上下文句子中与回答相关的比例（简化为 Token 覆盖）
    precision = len(tc & ta) / len(tc) if tc else 0.0
    recall = len(tc & ta) / len(ta) if ta else 0.0
    print("=" * 60)
    print("RAG 指标（RAGAS 简化实现，词重叠近似）：")
    print(f"  忠实度 Faithfulness      {faith:.2f}（回答是否忠于上下文）")
    print(f"  答案相关性 Relevance      {relevance:.2f}（是否切题）")
    print(f"  上下文精度 Precision     {precision:.2f}（检索是否相关）")
    print(f"  上下文召回 Recall        {recall:.2f}（关键信息是否召回）")
    print("提示：简化实现用词重叠近似语义，看趋势与对比有效，绝对值慎用（见 07 模块升级 RAGAS）")
    return 0


# ================= 回归对比 =================

def _load_results(path):
    if not os.path.exists(path):
        print(f"错误：文件不存在 {path}")
        return None
    try:
        with open(path, encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError as e:
        print(f"错误：JSON 解析失败 {e}")
        return None


def _agg_by_scenario(cases):
    """按场景聚合指标均值"""
    from collections import defaultdict
    agg = defaultdict(list)
    for case in cases:
        m = case.get("metrics") or {}
        for k, v in m.items():
            agg[(case.get("scenario", "未标注"), k)].append(v)
    result = {}
    for (scenario, metric), values in sorted(agg.items()):
        result.setdefault(scenario, {})[metric] = round(sum(values) / len(values), 3)
    return result


def cmd_compare(args):
    base = _load_results(args.base)
    new = _load_results(args.new)
    if base is None or new is None:
        return 2
    b_agg = _agg_by_scenario(base.get("cases", []))
    n_agg = _agg_by_scenario(new.get("cases", []))
    print("=" * 60)
    print(f"回归对比：{base.get('version', 'base')} vs {new.get('version', 'new')}")
    regress = []
    for scenario in sorted(set(b_agg) | set(n_agg)):
        bm, nm = b_agg.get(scenario, {}), n_agg.get(scenario, {})
        for metric in sorted(set(bm) | set(nm)):
            bv, nv = bm.get(metric), nm.get(metric)
            if bv is None or nv is None:
                continue
            delta = round(nv - bv, 3)
            mark = "↑" if delta > 0.01 else ("↓" if delta < -0.01 else "=")
            print(f"  [{scenario}] {metric}: {bv} → {nv} ({mark}{delta:+.3f})")
            if delta < -0.01:
                regress.append((scenario, metric, bv, nv, delta))
    if regress:
        print("⚠️ 退化项：")
        for s, m, bv, nv, d in regress:
            print(f"    [{s}] {m} {bv} → {nv}（{-d:.3f}）")
    else:
        print("✅ 无退化项")
    return 0


# ================= 报告与门禁 =================

def cmd_report(args):
    result = _load_results(args.result)
    if result is None:
        return 2
    gate = args.gate
    cases = result.get("cases", [])
    n = len(cases)
    suspicious = [c for c in cases if c.get("hallucination", "clean") != "clean"]
    agg = _agg_by_scenario(cases)
    print("=" * 60)
    print(f"评测报告：{result.get('version', 'unknown')}")
    print(f"  评测集规模：{n} 条　可疑样本：{len(suspicious)} 条")
    print("  分场景得分：")
    for scenario, metrics in agg.items():
        print(f"    [{scenario}] " + " ".join(f"{k}={v}" for k, v in metrics.items()))
    if suspicious:
        print("  Top 可疑样本（需人工复核）：")
        for c in suspicious[:5]:
            print(f"    [{c.get('id')}] {str(c.get('answer', ''))[:40]}")
    # 门禁判定
    blocked = False
    reasons = []
    if suspicious:
        high = [c for c in suspicious if (c.get("severity") or "medium") == "high"]
        if high:
            blocked = True
            reasons.append(f"高危可疑样本 {len(high)} 条")
    print("=" * 60)
    if blocked:
        print("门禁结论：❌ 拦截（" + "；".join(reasons) + "）")
        return 1
    print("门禁结论：✅ 通过（可疑样本需人工复核后确认）")
    return 0


def main():
    p = argparse.ArgumentParser(description="LLM 评测工具链（零依赖可运行）")
    sub = p.add_subparsers(dest="cmd")

    p_ds = sub.add_parser("dataset", help="评测集管理")
    p_ds.add_argument("--action", required=True, choices=["init", "check", "stat"])
    p_ds.add_argument("--out", default="evalset.jsonl", help="init 输出路径")
    p_ds.add_argument("--file", default="evalset.jsonl", help="check/stat 文件路径")

    p_hal = sub.add_parser("hallucination", help="幻觉检测")
    p_hal.add_argument("--answer", required=True, help="待检回答")
    p_hal.add_argument("--source", default="", help="来源/上下文（用于对照）")

    p_rag = sub.add_parser("ragscore", help="RAG 指标（RAGAS 简化）")
    p_rag.add_argument("--answer", required=True)
    p_rag.add_argument("--context", default="")
    p_rag.add_argument("--question", default="")

    p_cmp = sub.add_parser("compare", help="回归对比")
    p_cmp.add_argument("--base", required=True, help="基线结果 JSON")
    p_cmp.add_argument("--new", required=True, help="新结果 JSON")

    p_rep = sub.add_parser("report", help="报告与门禁")
    p_rep.add_argument("--result", required=True, help="评测结果 JSON")
    p_rep.add_argument("--gate", type=float, default=0.05, help="核心指标允许下降幅度")

    args = p.parse_args()
    if not args.cmd:
        p.print_help()
        return 0
    fn = {"dataset": lambda a: {"init": dataset_init, "check": dataset_check, "stat": dataset_stat}[a.action](a.out if a.action == "init" else a.file),
          "hallucination": cmd_hallucination, "ragscore": cmd_ragscore,
          "compare": cmd_compare, "report": cmd_report}[args.cmd]
    return fn(args)


if __name__ == "__main__":
    sys.exit(main())
