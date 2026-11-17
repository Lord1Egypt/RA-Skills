# -*- coding: utf-8 -*-
"""车辆驾驶自动化等级判定器 — 零依赖单文件 CLI · JSON IR 输出。
规则源：GB/T 40429-2021《汽车驾驶自动化分级》表1
定位：决策支持工具，非权威结论，须人工复核。
"""
import argparse, json, sys

META = {"slug": "aut-grade-checker", "version": "1.0.1", "args": [{"name": "dd", "help": "动态驾驶任务执行方: vehicle/driver/system", "required": False}, {"name": "oedr", "help": "目标事件探测响应方: vehicle/driver/system", "required": False}, {"name": "odd_limited", "help": "是否限定ODD: yes/no", "required": False}, {"name": "takeover_needed", "help": "是否需人工接管: yes/no", "required": False}, {"name": "both_axes", "help": "是否同时执行转向+加减速: yes/no", "required": False}]}

class GateError(Exception):
    pass

def _yes_no(v, name):
    """可选 yes/no 参数校验：未提供返回 None；提供但非法 → 门禁错误。"""
    v = (v or '').lower()
    if not v:
        return None
    if v not in ('yes', 'no'):
        raise GateError("%s 取值必须为 yes/no（当前：%s）" % (name, v))
    return v

def classify_aut(args):
    """车辆驾驶自动化等级 0-5 判定。规则源：GB/T 40429-2021《汽车驾驶自动化分级》表1。"""
    dd = (args.get('dd') or '').lower()
    oedr = (args.get('oedr') or '').lower()
    if not dd or not oedr:
        raise GateError("缺少必要参数：dd(动态驾驶任务执行方) 与 oedr(目标事件探测响应方) 必填，取值 system/driver（vehicle 视作 system）")
    if dd not in ('system', 'vehicle', 'driver'):
        raise GateError("dd 取值必须为 system/vehicle/driver（当前：%s）" % dd)
    if oedr not in ('system', 'driver', 'vehicle'):
        raise GateError("oedr 取值必须为 system/driver（vehicle 视作 system；当前：%s）" % oedr)
    odd = _yes_no(args.get('odd_limited'), 'odd_limited')
    takeover = _yes_no(args.get('takeover_needed'), 'takeover_needed')
    both = _yes_no(args.get('both_axes'), 'both_axes')
    sys_dd = dd in ('system', 'vehicle')   # 系统执行横向+纵向控制
    warns = []
    if sys_dd and oedr in ('system', 'vehicle'):
        # 系统完成全部 DD + OEDR
        possible = set()
        for o_cand in (odd, 'yes', 'no') if odd is None else (odd,):
            for t_cand in (takeover, 'yes', 'no') if takeover is None else (takeover,):
                if o_cand == 'no':
                    possible.add(5)
                elif t_cand == 'no':
                    possible.add(4)
                else:
                    possible.add(3)
        grade = max(possible)                # 从严推定：取可能等级中义务最重者
        if odd is None or takeover is None:
            warns.append(
                "输入不完整：odd_limited/takeover_needed 未提供（官方分级同时使用 ODD 限定与接管要求），"
                "建议补齐后复核。")
        if grade != min(possible):
            warns.append(
                "分类不确定（可能等级区间 L%d～L%d）：odd_limited/takeover_needed 参数不足，"
                "已按从严推定取『L%d』（义务最重者），实际等级可能更宽松；请补齐参数后复核。"
                % (min(possible), grade, grade))
    elif sys_dd and oedr == 'driver':
        # 系统执行 DD，驾驶员负责 OEDR
        if both is None:
            grade = 2                        # 从严推定：未说明是否双轴同时控制，取 L2
            warns.append(
                "分类不确定（可能等级区间 L1～L2）：未提供 both_axes，已按从严推定取『L2』"
                "（义务较重者），实际等级可能为 L1；请补齐参数后复核。")
        else:
            grade = 2 if both == 'yes' else 1   # 转向+加减速皆控→L2，否则→L1
    else:
        grade = 0              # 驾驶员负责全部，系统仅应急辅助
    resp = {
        0: "驾驶员全程负责（应急辅助）",
        1: "驾驶员负责OEDR与目标事件，系统提供部分辅助",
        2: "系统持续执行转向+加减速，驾驶员负责OEDR",
        3: "系统执行全部DD，有限ODD内运行，需后备用户接管",
        4: "系统执行全部DD+OEDR，有限ODD，系统自主应对",
        5: "系统在所有ODD执行全部DD+OEDR，无限制",
    }[grade]
    if grade in (3,4,5):
        warns.append("L3+ 不得宣称'自动驾驶/L2.9'等误导级别（'L2.9级'乱象可直接据此判定）")
    return {"grade": f"L{grade}", "responsibility": resp,
            "obligations": ["L3+ 须明示分级与责任边界", "宣传不得超实际等级标注"],
            "notes": ["以官方 GB/T 40429-2021 表1 为准", "企业/用户责任边界随等级变化",
                      "输入不足时按从严推定（取可能等级中义务最重者），不静默按宽松等级输出"],
            "evidence": ["GB/T 40429-2021 表1"], "warnings": warns}


def _run(args):
    res = classify_aut(args)
    warns = res.get("warnings") or []
    rc = 1 if warns else 0
    return res, rc

def main():
    p = argparse.ArgumentParser(prog="aut-grade-checker", description="车辆驾驶自动化等级判定器（决策支持·须人工复核）")
    for a in META["args"]:
        p.add_argument("--" + a["name"], required=False, help=a.get("help", ""))
    p.add_argument("--demo", action="store_true", help="跑内置冒烟案例")
    ns = p.parse_args()
    argnames = [a["name"] for a in META["args"]]
    AIGC = {"standard": "GB45438-2025", "is_generated": False, "generator": META["slug"] + "@SynomosAI",
             "content_type": "decision_support_output", "disclaimer": "决策支持非权威结论，须人工复核"}
    if ns.demo:
        demos = [{"dd": "system", "oedr": "system", "odd_limited": "yes", "takeover_needed": "yes"}, {"dd": "vehicle", "oedr": "driver", "both_axes": "yes"}]
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
