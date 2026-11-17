# -*- coding: utf-8 -*-
"""临床评价报告等同性论证要素检查器 — 零依赖单文件 CLI · JSON IR 输出。规则源：MDR (EU) 2017/745 Art 61 + Annex XIV Part A / MDCG 2020-5、2020-6 / MEDDEV 2.7/1 rev.4"""
import argparse
import json
import sys

META = {"slug": "cer-equivalence-check", "version": "1.0.0", "args": [{"name": "is_equivalent", "help": "是否采用等同器械路径: yes/no（必填）"}, {"name": "has_contract", "help": "是否具备等同器械数据访问权/合同: yes/no"}, {"name": "has_plan", "help": "含临床评价计划: yes/no"}, {"name": "has_lit_search", "help": "含文献检索方案与结果: yes/no"}, {"name": "has_appraisal", "help": "含数据评价与权重: yes/no"}, {"name": "has_analysis", "help": "含数据分析: yes/no"}, {"name": "has_conclusions", "help": "含结论与受益-风险判定: yes/no"}, {"name": "has_gap", "help": "含临床缺口与 PMCF 衔接: yes/no"}, {"name": "has_qualification", "help": "含评价者资质: yes/no"}, {"name": "has_update", "help": "含更新计划与日期: yes/no"}]}


class GateError(Exception):
    code = "E_RUNTIME"
    def __init__(self, msg, code=None):
        super().__init__(msg)
        if code:
            self.code = code


def check_cer(args):
    """CER 等同性论证要素检查。规则源：MDR Art 61 + Annex XIV Part A / MDCG 2020-5、2020-6 / MEDDEV 2.7/1 rev.4。"""
    is_eq = (args.get("is_equivalent") or "").lower()
    if is_eq not in ("yes", "no", "true", "false"):
        raise GateError("--is_equivalent 必填（yes/no）：是否采用等同器械路径", "E_INPUT_MISSING")
    sections = {
        "has_plan": "临床评价计划（CEP）",
        "has_lit_search": "文献检索方案与检索结果",
        "has_appraisal": "数据评价与权重（appraisal）",
        "has_analysis": "数据分析",
        "has_conclusions": "结论与受益-风险判定",
        "has_gap": "临床缺口与 PMCF 衔接",
        "has_qualification": "评价者资质",
        "has_update": "更新计划与日期",
    }
    missing = [cn for k, cn in sections.items() if (args.get(k) or "").lower() not in ("yes", "true", "1")]
    eq_checks, warns = [], []
    if is_eq in ("yes", "true"):
        eq_checks = [
            "技术等同：设计与制造、材料、性能、使用条件、灭菌方式等是否等同",
            "生物学等同：材料与生物相容性接触类型是否一致",
            "临床等同：临床使用场景、人群、部位、方法与预期效果是否一致",
        ]
        if (args.get("has_contract") or "").lower() not in ("yes", "true", "1"):
            warns.append("走等同器械路径但未见「等同器械数据访问权/合同」——Annex XIV Part A 要求充分访问权，缺失属重大缺陷")
    if missing:
        warns.append("CER 要素缺失：" + "、".join(missing) + "——技术评审高频发补点")
    oblig = [
        "CER 是技术文件的核心且须贯穿器械全生命周期持续更新",
        "等同性论证须三条同时成立（技术/生物学/临床），任一不成立即回退到自有临床数据",
        "MDR 下等同性论证的适用边界较旧指令显著收紧，须按 Art 61 与 MDCG 2020-5 复核",
    ]
    notes = [
        "本工具核查「要素是否在位」，不评价「论证是否成立」——后者须专业评价者判断",
        "NMPA 侧同品种比对与 MDR 侧等同性论证要求不同，不可直接互用",
        "等同器械可用范围以法规原文为准（如植入类/III 类的限制）",
    ]
    return {
        "path": "等同器械路径" if is_eq in ("yes", "true") else "自有临床数据路径",
        "equivalence_conditions": eq_checks,
        "missing_sections": missing, "complete": len(missing) == 0,
        "obligations": oblig, "notes": notes,
        "evidence": ["MDR (EU) 2017/745 Art 61 / Annex XIV Part A", "MDCG 2020-5", "MDCG 2020-6", "MEDDEV 2.7/1 rev.4"],
        "warnings": warns,
    }


def _call(args):
    fn_name = "check_cer"
    res = globals()[fn_name](args)
    return res


def main():
    p = argparse.ArgumentParser(prog="cer-equivalence-check", description="临床评价报告等同性论证要素检查器（决策支持·须人工复核）")
    for a in META["args"]:
        p.add_argument("--" + a["name"], required=False, default=None, help=a.get("help", ""))
    p.add_argument("--demo", action="store_true", help="跑内置冒烟案例")
    p.add_argument("--json", action="store_true", help="输出 JSON IR")
    ns = p.parse_args()
    names = [a["name"] for a in META["args"]]

    if ns.demo:
        ok = True
        for d in [{"is_equivalent": "yes", "has_contract": "yes", "has_plan": "yes", "has_lit_search": "yes", "has_appraisal": "yes", "has_analysis": "yes", "has_conclusions": "yes", "has_gap": "yes", "has_qualification": "yes", "has_update": "yes"}, {"is_equivalent": "yes", "has_contract": "no", "has_plan": "yes", "has_lit_search": "yes", "has_appraisal": "no", "has_analysis": "yes", "has_conclusions": "no", "has_gap": "no", "has_qualification": "yes", "has_update": "no"}]:
            try:
                res = _call(dict(d))
                rc = 1 if (res.get("warnings") or []) else 0
                print(json.dumps({"tool": META["slug"], "input": d, "result": res,
                                  "rc": rc, "error_code": None}, ensure_ascii=False))
            except GateError as e:
                ok = False
                print(json.dumps({"tool": META["slug"], "input": d, "errors": [str(e)],
                                  "rc": 2, "error_code": e.code}, ensure_ascii=False))
        sys.exit(0 if ok else 2)

    args = {k: getattr(ns, k) for k in names}
    if not any(v not in (None, "") for v in args.values()):
        p.print_help()
        sys.exit(0)
    try:
        res = _call(args)
    except GateError as e:
        print(json.dumps({"tool": META["slug"], "version": META["version"], "input": args,
                          "errors": [str(e)], "rc": 2, "error_code": e.code},
                         ensure_ascii=False, indent=2))
        sys.exit(2)
    rc = 1 if (res.get("warnings") or []) else 0
    ir = {"tool": META["slug"], "version": META["version"], "input": args,
          "result": res, "rc": rc, "error_code": None,
          "aigc_mark": {"standard": "GB 45438-2025", "is_generated": True,
                        "generator": META["slug"] + "@MedXpert",
                        "content_type": "decision_support_output",
                        "disclaimer": "决策支持非权威结论，须人工复核；以官方最新文件为准"}}
    print(json.dumps(ir, ensure_ascii=False, indent=2))
    sys.exit(rc)


if __name__ == "__main__":
    main()
