# -*- coding: utf-8 -*-
"""金融 AI 应用分级判定器 — 零依赖单文件 CLI · JSON IR 输出。
规则源：TH-FIN-002 母版（FDA SaMD 分级思维平移金融）+ 金融AI监管导向
定位：决策支持工具，非权威结论，须人工复核。
"""
import argparse, json, sys

META = {"slug": "fin-ai-classifier", "version": "1.0.1", "args": [{"name": "autonomy", "help": "自主度: full/human_in_loop/info", "required": False}, {"name": "impact", "help": "影响: high/mid/low", "required": False}, {"name": "target", "help": "对象: consumer/institution", "required": False}]}

class GateError(Exception):
    pass

# 等级严重度序（用于“从严推定”：输入不足时在可能等级中取义务最重者）
_GRADE_SEVERITY = ["I 级（低风险）", "II 级（中风险）", "III 级（高风险）"]

_OBLIG = {
    "III 级（高风险）": ["算法备案", "人工兜底 + 可解释", "模型与数据合规审计", "监管报送"],
    "II 级（中风险）": ["算法备案（依舆论属性）", "关键决策人工复核", "风险披露"],
    "I 级（低风险）": ["信息展示/营销须显著标识AI生成", "不得替代专业金融建议"],
}

def classify_fin(args):
    """金融 AI 应用分级判定。规则源：TH-FIN-002 母版（FDA SaMD 分级思维平移金融）+ 金融AI监管导向。"""
    autonomy = (args.get('autonomy') or '').lower()  # full/human_in_loop/info
    impact = (args.get('impact') or '').lower()      # high/mid/low
    target = (args.get('target') or '').lower()      # consumer/institution
    if autonomy and autonomy not in ('full', 'human_in_loop', 'info'):
        raise GateError("autonomy 取值必须为 full/human_in_loop/info（当前：%s）" % autonomy)
    if impact and impact not in ('high', 'mid', 'low'):
        raise GateError("impact 取值必须为 high/mid/low（当前：%s）" % impact)
    if target and target not in ('consumer', 'institution'):
        raise GateError("target 取值必须为 consumer/institution（当前：%s）" % target)

    # 完整参数下的直接判定（原实现规则，保持不变）
    def _grade_direct(aut, imp):
        if aut == 'full' and imp == 'high':
            return "III 级（高风险）"
        if aut == 'human_in_loop' and imp in ('high', 'mid'):
            return "II 级（中风险）"
        return "I 级（低风险）"

    # 输入不足 → 从严推定：枚举未知参数的所有合法补全，取可达等级中义务最重者
    aut_cands = ['full', 'human_in_loop', 'info'] if not autonomy else [autonomy]
    imp_cands = ['high', 'mid', 'low'] if not impact else [impact]
    possible = {_grade_direct(a, i) for a in aut_cands for i in imp_cands}
    naive = _grade_direct(autonomy or 'info', impact or 'low')
    strict = max(possible, key=_GRADE_SEVERITY.index)
    lenient = min(possible, key=_GRADE_SEVERITY.index)
    warnings = []
    grade = strict
    if strict != naive:
        missing = [n for n, v in (("autonomy", autonomy), ("impact", impact)) if not v]
        warnings.append(
            "输入不完整：未提供 %s；建议补齐后复核。" % " / ".join(missing))
        if strict != lenient:
            warnings.append(
                "分级不确定（可能区间 %s～%s）：已按从严推定取『%s』（义务最重者），"
                "实际等级可能更宽松；请补齐参数后复核。" % (lenient, strict, strict))
    else:
        grade = naive
    oblig = _OBLIG[grade]
    if grade.startswith("III"):
        warnings.append("全自动高影响面向消费者——须严格备案与人工兜底，禁止'AI 荐股/放贷'无资质经营")
    return {"grade": grade, "obligations": oblig,
            "notes": ["金融AI分级为监管前沿，以最新监管口径为准", "不得替代持牌机构专业意见",
                      "输入不足时按从严推定（取可能等级中义务最重者），不静默按宽松等级输出"],
            "evidence": ["TH-FIN-002 母版", "金融AI监管导向"], "warnings": warnings}


def _run(args):
    res = classify_fin(args)
    warns = res.get("warnings") or []
    rc = 1 if warns else 0
    return res, rc

def main():
    p = argparse.ArgumentParser(prog="fin-ai-classifier", description="金融 AI 应用分级判定器（决策支持·须人工复核）")
    for a in META["args"]:
        p.add_argument("--" + a["name"], required=False, help=a.get("help", ""))
    p.add_argument("--demo", action="store_true", help="跑内置冒烟案例")
    ns = p.parse_args()
    argnames = [a["name"] for a in META["args"]]
    AIGC = {"standard": "GB45438-2025", "is_generated": False, "generator": META["slug"] + "@SynomosAI",
             "content_type": "decision_support_output", "disclaimer": "决策支持非权威结论，须人工复核"}
    if ns.demo:
        demos = [{"autonomy": "full", "impact": "high", "target": "consumer"}, {"autonomy": "info", "impact": "low"}]
        allok = True
        out_list = []
        for d in demos:
            try:
                res, rc = _run(dict(d))
                out_list.append({"tool": META["slug"], "input": d, "result": res, "rc": rc, "aigc_mark": AIGC})
            except GateError as e:
                allok = False
                out_list.append({"tool": META["slug"], "input": d, "errors": [str(e)], "rc": 2, "aigc_mark": AIGC})
        print(json.dumps(out_list, ensure_ascii=False, indent=2))
        sys.exit(0 if allok else 2)
    args = {k: getattr(ns, k) for k in argnames}
    try:
        res, rc = _run(args)
    except GateError as e:
        ir = {"tool": META["slug"], "version": META["version"], "input": args, "errors": [str(e)], "rc": 2, "aigc_mark": AIGC}
        print(json.dumps(ir, ensure_ascii=False, indent=2))
        sys.exit(2)
    ir = {"tool": META["slug"], "version": META["version"], "input": args, "result": res, "rc": rc, "aigc_mark": AIGC}
    print(json.dumps(ir, ensure_ascii=False, indent=2))
    sys.exit(rc)

if __name__ == "__main__":
    main()
