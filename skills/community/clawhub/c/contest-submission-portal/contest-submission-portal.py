# -*- coding: utf-8 -*-
"""赛事作品提交合规校验器 — 零依赖单文件 CLI · JSON IR 输出。
规则源：UIBC 赛事提交规范（四规范·提交章）
定位：决策支持工具，非权威结论，须人工复核。
"""
import argparse, json, sys

META = {"slug": "contest-submission-portal", "version": "1.1.0", "args": [{"name": "track", "help": "赛道: code/theory/design", "required": False}, {"name": "files", "help": "提交文件清单(逗号分隔)", "required": False}, {"name": "format", "help": "主文件格式", "required": False}]}

class GateError(Exception):
    pass

def classify_submit(args):
    """赛事作品提交清单与格式合规性校验。规则源：UIBC 赛事提交规范（四规范·提交章）。"""
    track = (args.get('track') or '').lower()
    files = args.get('files') or ''
    fmt = (args.get('format') or '').lower()
    if not track:
        raise GateError("缺少必要参数：track(赛道, 如 code/theory/design) 必填")
    # 必交项与 SUBMISSION.md（提交章）严格对齐 v0.1：
    # code = .uibc 密封包 + seal.json 封签 + AIGC 声明 + RUN.md（攻击自述为加分项，另行提示）
    # theory 章程要求附最小可执行示例；design 章程要求附失败模式分析。
    required_spec = {
        'code': [('uibc-package', '.uibc', '`.uibc` 密封包（代码/文档/测试全入包）'),
                 ('seal', 'seal', 'seal.json 封签（作者自持 key 签封）'),
                 ('aigc', 'aigc', 'AIGC 声明（GB45438-2025）'),
                 ('run', 'run', 'RUN.md 复现步骤')],
        'theory': [('paper', 'paper', '规范/协议论文级提案'),
                   ('example', ('example', 'demo'), '最小可执行示例（章程硬要求）')],
        'design': [('design', 'design', '落地方案'),
                   ('failure', 'failure', '失败模式分析（章程硬要求）')],
    }
    spec = required_spec.get(track)
    file_list = [f.strip().lower() for f in files.split(',') if f.strip()]
    if spec is None:
        raise GateError("track 取值必须为 code/theory/design（当前：%s）" % track)
    else:
        required = [r[0] for r in spec]
        missing = []
        for key, pat, label in spec:
            pats = pat if isinstance(pat, tuple) else (pat,)
            if not any(p in f for f in file_list for p in pats):
                missing.append("%s(%s)" % (key, label))
    valid = len(missing) == 0
    fmt_ok = True
    fmt_warn = []
    # 格式白名单与 SUBMISSION.md 对齐：主文件 .md .py .json；证据任意（哈希入库）；
    # 禁止可执行二进制与外部网络依赖（离线可复现为硬约束）。
    allowed_map = {'code': 'md,py,json', 'theory': 'md,py,json,pdf',
                   'design': 'md,pdf,png,svg'}
    allowed = allowed_map.get(track, 'md,pdf')
    if not fmt:
        warnings_pre = ["未提供 format 参数：主文件格式未做白名单校验，请补齐后复核。"]
    else:
        warnings_pre = []
        if fmt not in allowed.split(','):
            fmt_ok = False
            fmt_warn.append("主文件格式 %s 不在赛道允许范围(%s)" % (fmt, allowed))
    exec_hits = [f for f in file_list if f.endswith(('.exe', '.dll', '.bat', '.ps1', '.so', '.bin'))]
    warnings = list(warnings_pre)
    if not valid:
        warnings.append("缺少必提交项：%s" % "; ".join(missing))
    if fmt and not fmt_ok:
        warnings.append(fmt_warn[0])
    if exec_hits:
        fmt_ok = False
        warnings.append("检测到可执行二进制 %s —— 提交规范禁止，直接退回" % ", ".join(exec_hits))
    bonus = [f for f in file_list if 'attack' in f or 'adversarial' in f]
    notes = ["必交项已与 SUBMISSION.md v0.1（提交章）对齐；以赛事章程最新版为准",
             "攻击自述为加分项（进 failure corpus 候选）" + ("：已检测到 %s" % ", ".join(bonus) if bonus else ""),
             "离线可复现为硬约束：禁止外部网络依赖"]
    return {"track": track, "required": required, "provided": file_list, "missing": missing,
            "valid": valid, "format_ok": fmt_ok, "warnings": warnings, "notes": notes,
            "evidence": ["UIBC 赛事提交规范·提交章 v0.1"]}


def _run(args):
    res = classify_submit(args)
    warns = res.get("warnings") or []
    rc = 1 if warns else 0
    return res, rc

def main():
    p = argparse.ArgumentParser(prog="contest-submission-portal", description="赛事作品提交合规校验器（决策支持·须人工复核）")
    for a in META["args"]:
        p.add_argument("--" + a["name"], required=False, help=a.get("help", ""))
    p.add_argument("--demo", action="store_true", help="跑内置冒烟案例")
    ns = p.parse_args()
    argnames = [a["name"] for a in META["args"]]
    AIGC = {"standard": "GB45438-2025", "is_generated": False, "generator": META["slug"] + "@SynomosAI",
             "content_type": "decision_support_output", "disclaimer": "决策支持非权威结论，须人工复核"}
    if ns.demo:
        demos = [{"track": "code", "files": "submission.uibc,seal.json,aigc-declaration.md,RUN.md,attack-report.md", "format": "py"}, {"track": "code", "files": "solution.py,readme.md", "format": "exe"}, {"track": "theory", "files": "paper.pdf,minimal-example.py", "format": "pdf"}]
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
