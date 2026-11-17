# -*- coding: utf-8 -*-
"""赛事反作弊身份核验器 — 零依赖单文件 CLI · JSON IR 输出。
规则源：UIBC 反作弊规范 + 通用学术诚信原则
定位：决策支持工具，非权威结论，须人工复核。
"""
import argparse, json, sys

META = {"slug": "anti-cheat-identity", "version": "1.1.0", "args": [{"name": "author_id", "help": "作者标识", "required": False}, {"name": "env_hash", "help": "环境指纹哈希", "required": False}, {"name": "prev_env_hashes", "help": "历史环境指纹 JSON 列表", "required": False}, {"name": "submit_count", "help": "同作者提交次数", "required": False}, {"name": "time_gap_min", "help": "距上次提交分钟", "required": False}]}

class GateError(Exception):
    pass

def classify_anticheat(args):
    """提交者身份与环境一致性核验（反作弊）。规则源：UIBC 反作弊规范 + 通用学术诚信。"""
    author = args.get('author_id') or ''
    env = args.get('env_hash') or ''
    prev_env = args.get('prev_env_hashes') or '[]'
    sc_raw = args.get('submit_count')
    try:
        submit_count = int(sc_raw) if sc_raw not in (None, '') else 1
    except (TypeError, ValueError):
        raise GateError("submit_count 必须为整数（同作者提交次数）")
    if submit_count < 1:
        raise GateError("submit_count 必须为正整数（≥1）")
    tg_raw = args.get('time_gap_min')
    try:
        time_gap_min = float(tg_raw) if tg_raw not in (None, '') else 9999.0
    except (TypeError, ValueError):
        raise GateError("time_gap_min 必须为数字（距上次提交分钟）")
    if time_gap_min < 0:
        raise GateError("time_gap_min 不应为负数，请核对输入")
    if not author or not env:
        raise GateError("缺少必要参数：author_id 与 env_hash 必填")
    try:
        prev = json.loads(prev_env) if isinstance(prev_env, str) else prev_env
    except Exception:
        raise GateError("prev_env_hashes 必须为 JSON 数组字符串（如 '[\"abc123\"]'）")
    if not isinstance(prev, list):
        raise GateError("prev_env_hashes 必须为 JSON 数组字符串（如 '[\"abc123\"]'）")
    flags = []
    risk = 'low'
    if prev and env not in prev:
        flags.append("环境指纹与历史不一致（疑似换设备/环境）")
        risk = 'mid'
    if prev and len(set(prev)) > 3:
        flags.append("历史环境指纹过多（疑似多环境轮换）")
        risk = 'high'
    if submit_count > 5:
        flags.append("同作者提交次数过高(%d)" % submit_count)
        risk = 'high'
    if time_gap_min < 10:
        flags.append("相邻提交间隔过短(%.0f分钟)" % time_gap_min)
        risk = 'high'
    advice = ("低风险：正常放行" if risk == 'low'
              else ("中风险：转人工抽检通道（机器门禁照跑，评审前人工抽检）" if risk == 'mid'
                    else "高风险：冻结提交通道并人工核查（冻结≠撤销，处置记录须留痕）"))
    return {"author_id": author, "risk_level": risk, "flags": flags, "advice": advice,
            "warnings": flags,
            "notes": ["环境指纹为设备/网络特征哈希，不存明文",
                      "分级处置口径：low 放行 / mid 人工抽检 / high 冻结（对齐赛事章程）",
                      "最终裁定权归组委会（不可让渡）"],
            "evidence": ["UIBC 反作弊规范"]}


def _run(args):
    res = classify_anticheat(args)
    warns = res.get("warnings") or []
    rc = 1 if warns else 0
    return res, rc

def main():
    p = argparse.ArgumentParser(prog="anti-cheat-identity", description="赛事反作弊身份核验器（决策支持·须人工复核）")
    for a in META["args"]:
        p.add_argument("--" + a["name"], required=False, help=a.get("help", ""))
    p.add_argument("--demo", action="store_true", help="跑内置冒烟案例")
    ns = p.parse_args()
    argnames = [a["name"] for a in META["args"]]
    AIGC = {"standard": "GB45438-2025", "is_generated": False, "generator": META["slug"] + "@SynomosAI",
             "content_type": "decision_support_output", "disclaimer": "决策支持非权威结论，须人工复核"}
    if ns.demo:
        demos = [{"author_id": "teamA", "env_hash": "abc123", "prev_env_hashes": "[\"abc123\"]", "submit_count": "1", "time_gap_min": "120"}, {"author_id": "teamB", "env_hash": "xyz999", "prev_env_hashes": "[\"a1\",\"a2\",\"a3\",\"a4\",\"a5\"]", "submit_count": "8", "time_gap_min": "3"}]
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
