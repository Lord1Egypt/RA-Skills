# -*- coding: utf-8 -*-
"""电子证据四性审查判定器 — 零依赖单文件 CLI · JSON IR 输出。

规则源（**条款号与适用范围均待人工核对**，见输出字段 clause_review_checklist）：
  最高人民法院《关于民事诉讼证据的若干规定》 第14条 / 第93-95条（条款号待人工核对）
  《人民法院在线诉讼规则》 第12-18条（条款号待人工核对）

定位：决策支持工具，非权威结论、**不构成法律意见**；最终采信由司法机关认定。
一律以官方最新文本为准。
"""
import argparse, json, sys

META = {
    "slug": "evid-four-check",
    "version": "1.0.0",
    # required 策略：本工具 5 个参数**全部** required=False，原因：
    #  ① 单个参数缺失正是 rc=1「从严推定」的触发条件（取可能判定中义务最重者）；
    #  ② 若把某参数改为 required=True，argparse 会在解析阶段直接退出并打印 usage（非 JSON IR），
    #     破坏 rc 三档语义（rc=2 必须也走 JSON IR）。
    # main() 逐条读取本字段并传给 argparse ⇒ 元数据与行为一致（后续把某项改 True 即生效）。
    "args": [
        {"name": "type", "help": "证据类型(如 合同/聊天记录/邮件/日志/音视频)", "required": False},
        {"name": "has_signature", "help": "有电子签名/可信时间戳/区块链存证: yes/no", "required": False},
        {"name": "source_verifiable", "help": "来源可验证(可回溯原始载体/系统): yes/no", "required": False},
        {"name": "integrity_check", "help": "完整性哈希校验: yes/no", "required": False},
        {"name": "relevance", "help": "与待证事实关联: yes/no", "required": False},
    ],
}

# 四性维度（固定顺序，保证输出稳定、便于逐次比对）
DIMENSIONS = ["真实性", "合法性", "关联性", "完整性"]

# 各维度：由哪些参数驱动 / 规则出处（条款依据，非本案证据记录）/ 缺参时的补参建议
DIM_META = {
    "真实性": {
        "args": ["has_signature", "source_verifiable"],
        "any_pass": True,   # 签名/存证 或 来源可验证，满足其一即通过
        "rule_sources": ["证据规定 第14条", "证据规定 第93-95条", "在线诉讼规则 第12-18条"],
        "hint": "--has_signature yes|no（电子签名/可信时间戳/区块链存证 之一即有）"
                " 或 --source_verifiable yes|no（来源可回溯原始载体/系统）",
    },
    "合法性": {
        "args": ["type"],
        "any_pass": False,
        "rule_sources": ["证据规定 第14条", "在线诉讼规则 第12-18条"],
        "hint": "--type 合同|聊天记录|邮件|日志|音视频（声明证据类型，仅做形式审查）",
    },
    "关联性": {
        "args": ["relevance"],
        "any_pass": False,
        "rule_sources": ["证据规定 第14条"],
        "hint": "--relevance yes|no（证据与待证事实是否相关）",
    },
    "完整性": {
        "args": ["integrity_check"],
        "any_pass": False,
        "rule_sources": ["证据规定 第93-95条", "在线诉讼规则 第12-18条"],
        "hint": "--integrity_check yes|no（是否提供哈希值/原始载体比对）",
    },
}

# 条款号待人工核对清单：哪一条款用于什么判定（随输出一并给出，便于人工复核）
CLAUSE_CHECKLIST = [
    {"clause": "证据规定 第14条", "used_for": "电子数据范围（含网络平台发布信息、通讯信息、电子文件等）的界定",
     "status": "待人工核对"},
    {"clause": "证据规定 第93条", "used_for": "电子数据真实性审查的考虑因素（载体、生成方式、保存方法等）",
     "status": "待人工核对"},
    {"clause": "证据规定 第94条", "used_for": "真实性推定情形（第三方平台存证、中立系统、公证等）",
     "status": "待人工核对"},
    {"clause": "证据规定 第95条", "used_for": "一方控制证据而拒不提交的法律后果（本条对应举证妨碍，非直接的四性判定）",
     "status": "待人工核对"},
    {"clause": "在线诉讼规则 第12条～第18条", "used_for": "在线诉讼中电子化材料的提交、原件认定、区块链存证与上链真实性审查",
     "status": "待人工核对"},
    {"clause": "GB 45438-2025", "used_for": "AIGC 标识字段 aigc_mark 的标注依据",
     "status": "待人工核对"},
    {"clause": "「四性」维度划分（真实/合法/关联/完整）", "used_for": "本工具的输出结构；属审查清单口径，**非任何条文原文表述**",
     "status": "待人工核对"},
]

# 输出语义（固定文案，避免歧义与过度声称）
CONCLUSION_PASS = "四性形式审查均通过（不构成证据能力或采信结论；最终采信由司法机关认定）"
CONCLUSION_FAIL = "四性形式审查存在未通过项，证据能力待补强（不构成证据能力或采信结论；最终采信由司法机关认定）"

NOTES = [
    "本工具仅做**规则判定的形式审查**，不做法律意见，也不构成任何权威结论；最终采信由司法机关认定。",
    "「合法性」本次仅做形式审查（是否已声明证据类型），**不含取证手段合法性（窃录/侵入/超范围取证等）的实体判断**；"
    "涉该项须另行审查。",
    "「证据能力/证明力」的实质判断、公证书与鉴定意见的效力、对方质证意见，均不在本工具覆盖范围内。",
    "输入不完整时按**从严推定**（对缺失维度取「未通过（待补强）」），并在 warnings 中给出可能区间与补参建议；"
    "不静默按宽松结论输出。",
    "输出字段 evidence / rule_sources 为**规则出处（条款依据）**，不是本案证据记录，也不记录任何取证行为。",
    "条款号与维度口径**均待人工核对**（见 clause_review_checklist）；一律以官方最新文本为准。",
]

YES_TOKENS = {"yes", "y", "true", "1", "是", "有"}
NO_TOKENS = {"no", "n", "false", "0", "否", "无"}


class GateError(Exception):
    """输入门禁错误 ⇒ rc=2（输入非法/输入不足，无法判定）。"""


def _flag(value, name):
    """归一化 yes/no 型参数。

    返回 None=未提供（触发从严推定）；True/False=明确取值；
    其它取值 ⇒ GateError（rc=2 输入非法），不猜测、不静默当 no。
    """
    if value is None:
        return None
    s = str(value).strip().lower()
    if s == "":
        return None
    if s in YES_TOKENS:
        return True
    if s in NO_TOKENS:
        return False
    raise GateError("参数 --%s 取值非法：%r；仅接受 yes/no（也接受 y/n、true/false、是/否、有/无）" % (name, value))


def _dim(value_map, dim):
    """对单个维度做判定，返回 (PASS/FAIL, 是否「从严推定」, 是否缺参)。

    从严推定的形式化口径：该维判定为 FAIL，且驱动它的参数中至少有一个未提供
    （即补齐参数后该维**可能**转为 PASS）⇒ 属不确定区间，取义务最重者（FAIL）。
    """
    meta = DIM_META[dim]
    vals = [value_map[a] for a in meta["args"]]
    passed = any(v is True for v in vals) if meta["any_pass"] else all(v is True for v in vals)
    uncertain = (not passed) and any(v is None for v in vals)
    return ("PASS" if passed else "FAIL"), uncertain, any(v is None for v in vals)


def classify_evid(args):
    """电子证据四性审查（JSON IR 结果体）。

    规则源：最高人民法院《关于民事诉讼证据的若干规定》第14条/第93-95条
            + 《人民法院在线诉讼规则》第12-18条（条款号均待人工核对）。
    """
    raw_type = args.get("type")
    typ = None if raw_type is None else str(raw_type).strip()
    if typ == "":
        typ = None

    flags = {
        "has_signature": _flag(args.get("has_signature"), "has_signature"),
        "source_verifiable": _flag(args.get("source_verifiable"), "source_verifiable"),
        "integrity_check": _flag(args.get("integrity_check"), "integrity_check"),
        "relevance": _flag(args.get("relevance"), "relevance"),
    }
    value_map = {"type": True if typ is not None else None}
    value_map.update(flags)

    if typ is None and all(v is None for v in flags.values()):
        raise GateError("缺少必要参数：请至少提供 --type，或 --has_signature / --source_verifiable "
                        "/ --integrity_check / --relevance 之一（yes/no）")

    four, basis, missing_dims, certain_fail_dims = {}, {}, [], []
    for dim in DIMENSIONS:
        verdict, uncertain, has_missing = _dim(value_map, dim)
        four[dim] = verdict
        if uncertain:
            basis[dim] = "从严推定（输入不完整）"
            missing_dims.append(dim)
        elif has_missing:
            # 参数缺失但该维已确定 PASS（例如真实性已由 has_signature=yes 满足）
            basis[dim] = "明确输入（部分参数未提供，但不影响本维结论）"
        else:
            basis[dim] = "明确输入"
        if verdict == "FAIL" and not uncertain:
            certain_fail_dims.append(dim)

    all_pass = all(v == "PASS" for v in four.values())
    conclusion = CONCLUSION_PASS if all_pass else CONCLUSION_FAIL
    possible = [CONCLUSION_PASS] if all_pass else [CONCLUSION_PASS, CONCLUSION_FAIL]

    # ---- 补强建议（remediation）----
    REMEDY = {
        "真实性": "补强：提供电子签名 / 可信时间戳 / 区块链存证记录，或可回溯的原始载体与生成、保存、传输方法说明",
        "合法性": "补强：声明并说明证据类型与来源；取证手段合法性须另行人工审查（本工具不作实体判断）",
        "关联性": "补强：说明证据与待证事实的逻辑关联及证明目的",
        "完整性": "补强：提供哈希值（摘要）与原始载体比对，说明是否经篡改、增删",
    }
    remediation = []
    for dim in DIMENSIONS:
        if four[dim] == "FAIL":
            tag = "（按从严推定未通过；补齐参数后可能转为通过）" if basis[dim].startswith("从严推定") else "（经输入明确判定未通过）"
            remediation.append(REMEDY[dim] + tag)

    # ---- 告警（warnings）—— rc=1 的唯一来源，非空即 rc=1 ----
    warnings = []
    if missing_dims:
        warnings.append(
            "输入不完整：未提供判定「%s」所需的全部参数；已按**从严推定**取『FAIL（待补强）』"
            "（可能判定中义务最重者）。" % "、".join(missing_dims))
        warnings.append(
            "可能区间：%s 在补齐参数后**可能为 PASS～FAIL**（当前按从严取 FAIL）；"
            "整体结论区间为『四性形式审查均通过』～『存在未通过项，待补强』。"
            % "、".join(missing_dims))
        hints = [DIM_META[d]["hint"] for d in missing_dims]
        warnings.append("补参建议：%s；补齐后请复核，勿以本次结论代替完整判定。" % "；".join(hints))
    if certain_fail_dims:
        warnings.append(
            "经输入明确判定「%s」未通过：该判定基于你提供的明确取值（非从严推定）；"
            "补强建议见 remediation。" % "、".join(certain_fail_dims))
    if not all_pass:
        warnings.append(
            "本结论为**形式审查**结果，不构成证据能力认定，也不代表已被采信；"
            "最终由司法机关认定（本工具不含取证手段合法性、证明力大小的实体判断）。")

    rule_sources = sorted({s for d in DIMENSIONS for s in DIM_META[d]["rule_sources"]})

    return {
        "four_properties": four,
        "dimension_basis": basis,
        "possible_conclusions": possible,
        "conclusion": conclusion,
        "remediation": remediation,
        "missing_inputs": [a for a, v in value_map.items() if v is None],
        "evidence": rule_sources,          # 规则出处（条款依据）——不是本案证据记录
        "notes": NOTES,
        "warnings": warnings,
    }


def _run(args):
    """返回 (结果体, rc)。rc 语义：0=正常无告警 / 1=完成但带告警（含从严推定）/ 2=门禁错误。"""
    res = classify_evid(args)
    warns = res.get("warnings") or []
    rc = 1 if warns else 0
    return res, rc


def main():
    p = argparse.ArgumentParser(prog="evid-four-check", description="电子证据四性审查判定器（决策支持·须人工复核）")
    for a in META["args"]:
        # 逐条读取 META 的 required（不再硬编码 False），元数据与行为一致
        p.add_argument("--" + a["name"], required=a.get("required", False), help=a.get("help", ""))
    p.add_argument("--demo", action="store_true", help="跑内置冒烟案例")
    ns = p.parse_args()
    argnames = [a["name"] for a in META["args"]]
    # AIGC 标识：输出由工具生成（确定性规则计算 + AI 辅助撰写规则文本）⇒ is_generated=True；
    # 具体标注口径（是否属 GB 45438-2025 意义上的「生成合成内容」）待人工核对，见 label_note。
    AIGC = {"standard": "GB 45438-2025", "is_generated": True,
            "generator": META["slug"] + "@SynomosAI",
            "content_type": "decision_support_output",
            "label_note": "标识口径待核：输出由确定性规则代码计算，规则文本为 AI 辅助撰写",
            "disclaimer": "决策支持非权威结论，须人工复核"}
    if ns.demo:
        demos = [
            {"type": "电子合同", "has_signature": "yes", "source_verifiable": "yes",
             "integrity_check": "yes", "relevance": "yes"},                                   # rc=0
            {"type": "聊天记录", "has_signature": "no", "integrity_check": "no",
             "relevance": "yes"},                                                              # rc=1（缺 source_verifiable → 从严）
            {"has_signature": "yes", "integrity_check": "yes", "relevance": "yes"},            # rc=1（缺 type → 合法性从严）
        ]
        allok = True
        out_list = []
        for d in demos:
            try:
                res, rc = _run(dict(d))
                out_list.append({"tool": META["slug"], "input": d, "result": res, "rc": rc,
                                 "clause_review_checklist": CLAUSE_CHECKLIST, "aigc_mark": AIGC})
            except GateError as e:
                allok = False
                out_list.append({"tool": META["slug"], "input": d, "errors": [str(e)], "rc": 2,
                                 "clause_review_checklist": CLAUSE_CHECKLIST, "aigc_mark": AIGC})
        print(json.dumps(out_list, ensure_ascii=False, indent=2))
        # 进程退出码遵循本技能库约定：0＝案例全部执行完毕 / 2＝存在输入错误。
        # 各案例的实际 rc 见 IR 的 rc 字段（可为 0/1/2），--demo 不代替单次调用的 rc 语义。
        sys.exit(0 if allok else 2)
    args = {k: getattr(ns, k) for k in argnames}
    try:
        res, rc = _run(args)
    except GateError as e:
        ir = {"tool": META["slug"], "version": META["version"], "input": args, "errors": [str(e)], "rc": 2,
              "clause_review_checklist": CLAUSE_CHECKLIST, "aigc_mark": AIGC}
        print(json.dumps(ir, ensure_ascii=False, indent=2))
        sys.exit(2)
    ir = {"tool": META["slug"], "version": META["version"], "input": args, "result": res, "rc": rc,
          "clause_review_checklist": CLAUSE_CHECKLIST, "aigc_mark": AIGC}
    print(json.dumps(ir, ensure_ascii=False, indent=2))
    sys.exit(rc)


if __name__ == "__main__":
    main()
