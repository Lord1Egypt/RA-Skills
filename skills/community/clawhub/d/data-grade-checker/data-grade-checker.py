# -*- coding: utf-8 -*-
"""数据分类分级判定器 — 零依赖单文件 CLI · JSON IR 输出。
规则源：GB/T 43697-2024《数据安全技术 数据分类分级规则》(2024-10-01实施)
定位：决策支持工具，非权威结论，须人工复核。
"""
import argparse, json, sys

META = {"slug": "data-grade-checker", "version": "1.0.1", "args": [{"name": "industry", "help": "行业: finance/energy/transport/bio/health/geo/population/gov/key_infra 等", "required": False}, {"name": "core_interest", "help": "是否涉及国家核心利益: yes/no", "required": False}, {"name": "scale", "help": "规模/敏感度: high/mid/low", "required": False}, {"name": "cross_border", "help": "是否出境: yes/no", "required": False}]}

class GateError(Exception):
    pass

# 等级严重度序（用于“从严推定”：输入不足时在可能等级中取义务最重者）
_GRADE_SEVERITY = ["一般数据", "重要数据", "核心数据"]

def classify_data(args):
    """数据分类分级判定。规则源：GB/T 43697-2024《数据安全技术 数据分类分级规则》(2024-10-01实施)。"""
    industry = (args.get('industry') or '').lower()
    core = args.get('core_interest')  # 是否涉及国家核心利益: yes/no
    scale = args.get('scale')         # 规模/敏感度: high/mid/low
    cross = args.get('cross_border')  # 是否出境: yes/no
    if core is not None and core not in ('yes', 'no'):
        raise GateError("core_interest 取值必须为 yes/no（当前：%s）" % core)
    if cross is not None and cross not in ('yes', 'no'):
        raise GateError("cross_border 取值必须为 yes/no（当前：%s）" % cross)
    if scale is not None and scale not in ('high', 'mid', 'low'):
        raise GateError("scale 取值必须为 high/mid/low（当前：%s）" % scale)

    _OBLIG = {
        "核心数据": ["出境安全评估 + 审批", "最高级保护义务", "原则上不得出境"],
        "重要数据": ["分类分级管理 + 加密", "出境安全评估/备案", "重要数据目录报送", "定期风险评估"],
        "一般数据": ["基础保护义务（保密/完整/可用）", "出境按个保法/标准合同办理"],
    }
    _IMPORTANT_INDUSTRIES = ('finance','energy','transport','bio','health','geo','population','gov','key_infra')

    # 完整参数下的直接判定（原实现规则，保持不变）
    def _grade_direct(core_v, industry_v, scale_v):
        if core_v == 'yes':
            return "核心数据"
        if industry_v in _IMPORTANT_INDUSTRIES or scale_v == 'high':
            return "重要数据"
        return "一般数据"

    # 输入不足 → 从严推定：枚举未知参数的所有合法补全，取可达等级中义务最重者
    core_cands = ['yes', 'no'] if core is None else [core]
    industry_cands = list(_IMPORTANT_INDUSTRIES) + ['other'] if industry == '' else [industry]
    scale_cands = ['high', 'mid', 'low'] if scale is None else [scale]
    possible = set()
    for c in core_cands:
        for i in industry_cands:
            for s in scale_cands:
                possible.add(_grade_direct(c, i, s))
    naive = _grade_direct(core if core is not None else 'no', industry, scale)
    strict = max(possible, key=_GRADE_SEVERITY.index)
    lenient = min(possible, key=_GRADE_SEVERITY.index)
    warnings = []
    grade = strict
    if strict != naive:
        if core is None:
            warnings.append(
                "输入不完整：未说明是否涉及国家核心利益（core_interest），该参数可触发最高级；"
                "建议补齐 core_interest / industry / scale 后复核。")
        else:
            warnings.append(
                "输入不完整：仅提供部分参数（缺 core_interest / scale 中未给项），"
                "建议补齐后复核。")
        if strict != lenient:
            warnings.append(
                "分级不确定（可能区间 %s～%s）：已按从严推定取『%s』（义务最重者），"
                "实际等级可能更宽松；请补齐参数后复核。" % (lenient, strict, strict))
    else:
        grade = naive
    oblig = _OBLIG[grade]
    if cross in ('yes', True) and grade != "一般数据":
        warnings.append("出境须走数据出境安全评估/标准合同/认证路径")
    return {"grade": grade, "obligations": oblig,
            "notes": ["行业敏感清单以官方附录为准", "跨部门数据按'就高'原则定级",
                      "输入不足时按从严推定（取可能等级中义务最重者），不静默按宽松等级输出"],
            "evidence": ["GB/T 43697-2024"], "warnings": warnings}


def _run(args):
    res = classify_data(args)
    warns = res.get("warnings") or []
    rc = 1 if warns else 0
    return res, rc

def main():
    p = argparse.ArgumentParser(prog="data-grade-checker", description="数据分类分级判定器（决策支持·须人工复核）")
    for a in META["args"]:
        p.add_argument("--" + a["name"], required=False, help=a.get("help", ""))
    p.add_argument("--demo", action="store_true", help="跑内置冒烟案例")
    ns = p.parse_args()
    argnames = [a["name"] for a in META["args"]]
    AIGC = {"standard": "GB45438-2025", "is_generated": False, "generator": META["slug"] + "@SynomosAI",
             "content_type": "decision_support_output", "disclaimer": "决策支持非权威结论，须人工复核"}
    if ns.demo:
        demos = [{"core_interest": "yes"}, {"industry": "finance", "scale": "high"}, {"industry": "retail"}]
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
