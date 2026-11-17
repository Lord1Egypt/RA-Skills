#!/usr/bin/env python3
"""
bidhunter.py - Unified zero-friction entry point (BidHunter v1.5, A9).

Wraps the most common operations behind one memorable command so non-technical
users don't need to remember pipeline.sh / qual_check.py flags.

Usage:
  python3 bidhunter.py run [--fresh] [--summary]      # 采集+比对+报告+推送
  python3 bidhunter.py status                          # 今日采集状态
  python3 bidhunter.py doctor                          # 一键诊断
  python3 bidhunter.py demo                            # 看示例效果
  python3 bidhunter.py calendar [--days 7]             # 投标日历
  python3 bidhunter.py faq [关键词]                     # 查常见问题
  python3 bidhunter.py rules edit [--port 8080]        # 打开规则编辑器
  python3 bidhunter.py ai read <招标文件.pdf>          # v2.0 AI 速读（分片全覆盖）
  python3 bidhunter.py gap scan <招标文件.pdf>         # v2.8 待补材料清单（高危红标）
  python3 bidhunter.py gap zero <投标文件草稿>        # v2.8 零响应检测（空洞/待补/残留）
  python3 bidhunter.py score ledger <招标文件.pdf>     # v2.9 评分点台账（五态+四报警）
  python3 bidhunter.py score coverage <招标文件.pdf>   # v2.9 正向覆盖矩阵（A/B/C 三档）
  python3 bidhunter.py ai advise <招标文件.pdf>        # v2.5 投标建议
  python3 bidhunter.py api serve [--port 8765]         # v3.0 本地查询API
  python3 bidhunter.py compliance scan <标书.pdf>       # v3.5 合规红线扫描
  python3 bidhunter.py compliance checklist            # v3.5 交标前自查清单
  python3 bidhunter.py quote params                     # v2.7 报价参数库（首次填一次）
  python3 bidhunter.py quote check --help                # v2.7 报价闸门（不过禁止出金额）
  python3 bidhunter.py init [--preview]                 # v2.6 首次运行引导（三问生成配置）
  python3 bidhunter.py paste <招标文件.pdf>             # v2.6 零配置出废标风险报告（离线可跑）
  python3 bidhunter.py usage [--funnel]                 # v2.6 本地埋点统计（仅写本地）
  python3 bidhunter.py help                            # 全部命令
"""
import os
import sys
import subprocess
import argparse

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PY = sys.executable


def _track(event):
    """本地埋点（仅写本地文件，任何失败静默）"""
    try:
        from usage import track
        track(event)
    except Exception:
        pass


def _run(cmd, **kw):
    return subprocess.run([PY, "-u", os.path.join(SCRIPT_DIR, cmd)] + kw.get("args", []),
                          capture_output=kw.get("capture", False), text=True)


def cmd_run(args):
    extra = []
    if args.fresh:
        extra.append("--fresh")
    if args.summary:
        extra.append("--summary")
    r = subprocess.run(["bash", os.path.join(SCRIPT_DIR, "pipeline.sh")] + extra)
    return r.returncode


def cmd_status(args):
    r = _run("status.py", capture=True)
    print(r.stdout or r.stderr)
    return 0


def cmd_doctor(args):
    r = _run("doctor.py")
    return r.returncode


def cmd_demo(args):
    _track("demo_start")
    r = _run("demo.py", args=(["--summary", "--calendar"] if args.calendar else []))
    _track("demo_done")
    return 0


def cmd_init(args):
    """首次运行引导：三问生成资质规则库与采集源骨架（行业自由输入，不设固定模板）"""
    _track("init_start")
    extra = ["--preview"] if args.preview else []
    r = _run("init_wizard.py", args=extra)
    return r.returncode


def cmd_paste(args):
    """零配置兜底：丢一份招标文件进来直接出废标风险报告（不依赖 AI key，离线可跑）"""
    f = args.file
    if not f:
        print("[error] 需要文件路径，用法：python3 bidhunter.py paste <文件.pdf>",
              file=sys.stderr)
        return 1
    if not os.path.exists(f):
        print(f"[error] 文件不存在: {f}", file=sys.stderr)
        return 1
    extra = [f]
    if args.mode:
        extra += ["--mode", args.mode]
    if args.json:
        extra.append("--json")
    r = _run(os.path.join("compliance", "compliance_scanner.py"), args=extra)
    if r.returncode == 0:
        _track("paste_done")
    return r.returncode


def cmd_usage(args):
    """本地埋点统计（仅写本地，绝不外传）"""
    r = _run("usage.py", args=(["funnel"] if args.funnel else []), capture=True)
    print(r.stdout or r.stderr)
    return 0


def cmd_calendar(args):
    # use today's qual file if present
    import glob
    files = sorted(glob.glob(os.path.join(SCRIPT_DIR, "bid_cache", "qual_*.jsonl")))
    target = files[-1] if files else None
    if not target:
        print("尚无 qual 数据，请先运行: python3 bidhunter.py run")
        return 1
    r = _run("calendar.py", args=[target, "--days", str(args.days)])
    if r.stdout:
        print(r.stdout)
    return 0


def cmd_faq(args):
    r = _run("faq.py", args=(args.terms if args.terms else []), capture=True)
    print(r.stdout or r.stderr)
    return 0


def cmd_rules(args):
    if args.action == "edit":
        port = args.port
        print(f"启动规则编辑器 → http://localhost:{port}  (Ctrl+C 退出)")
        r = _run("rule_editor.py", args=["--port", str(port)])
        return r.returncode
    print("用法: python3 bidhunter.py rules edit [--port 8080]")
    return 1


def cmd_ai(args):
    if args.action == "read":
        r = _run("ai/doc_reader.py", args=[args.file])
        if r.stdout:
            print(r.stdout)
        return r.returncode
    if args.action == "advise":
        r = _run("ai/bid_advisor.py", args=[args.file])
        if r.stdout:
            print(r.stdout)
        return r.returncode
    print("用法: bidhunter.py ai read <文件> | ai advise <文件>")
    return 1


def cmd_api(args):
    if args.action == "serve":
        r = _run("api_server.py", args=["--port", str(args.port)])
        return r.returncode
    print("用法: bidhunter.py api serve [--port 8765]")
    return 1


def cmd_gap(args):
    """v2.8 待补材料清单 + 零响应检测（纯规则，零 API 成本）"""
    sc = "material_gap.py"
    if args.action == "scan":
        if not args.file:
            print("用法: bidhunter.py gap scan <招标文件> [--json]")
            return 1
        a = ["gap", args.file]
        if args.json:
            a.append("--json")
    elif args.action == "zero":
        if not args.file:
            print("用法: bidhunter.py gap zero <投标文件草稿> [--json]"
                  " [--our-project 名称] [--other-projects 名称 ...]")
            return 1
        a = ["zero", args.file]
        if args.json:
            a.append("--json")
        if args.our_project:
            a += ["--our-project", args.our_project]
        if args.other_projects:
            a += ["--other-projects"] + list(args.other_projects)
    else:
        print("用法:")
        print("  bidhunter.py gap scan <招标文件>        # 待补材料清单（高危项红标）")
        print("  bidhunter.py gap zero <投标文件草稿>    # 零响应检测（空洞满足/待补占位/项目残留）")
        print("  bidhunter.py gap scan <标书> --json     # 机器可读输出")
        return 0
    r = _run(sc, args=a)
    if r.stdout:
        print(r.stdout)
    return r.returncode


def cmd_score(args):
    """v2.9 评分点台账 + 正向覆盖矩阵（纯规则，零 API 成本）"""
    sc = "score_ledger.py"
    if args.action == "selftest":
        r = _run(sc, args=["--selftest"])
        return r.returncode
    if not args.action:
        print("用法:")
        print("  bidhunter.py score ledger <招标文件>     # B1 评分点台账（五态+四条必报警）")
        print("  bidhunter.py score coverage <招标文件>   # B2 正向覆盖矩阵（A/B/C）")
        print("  bidhunter.py score both <招标文件>       # 两张表一起出")
        print("  ... --json / --csv P / --xlsx P / --deadline YYYY-MM-DD / --materials F")
        print("  bidhunter.py score selftest              # 内置自测")
        return 0
    a = [args.action]
    if args.file:
        a.append(args.file)
    if args.json:
        a.append("--json")
    if args.csv:
        a += ["--csv", args.csv]
    if args.xlsx:
        a += ["--xlsx", args.xlsx]
    if args.from_json:
        a += ["--from-json", args.from_json]
    if args.materials:
        a += ["--materials", args.materials]
    if args.response:
        a += ["--response", args.response]
    if args.prev_ledger:
        a += ["--prev-ledger", args.prev_ledger]
    if args.deadline:
        a += ["--deadline", args.deadline]
    if args.confirm_regress:
        a.append("--confirm-regress")
    r = _run(sc, args=a)
    if r.stdout:
        print(r.stdout)
    return r.returncode


def cmd_compliance(args):
    """v3.5 合规红线扫描（本地规则库，零 API 成本）"""
    sc = "compliance/compliance_scanner.py"
    if args.action == "scan":
        if not args.file:
            print("用法: bidhunter.py compliance scan <文件> [--mode tender|bid|both] [--json] [--llm]")
            return 1
        a = [args.file, "--mode", args.mode]
        if args.json:
            a.append("--json")
        if args.llm:
            a.append("--llm")
        r = _run(sc, args=a)
        if r.stdout:
            print(r.stdout)
        return r.returncode
    if args.action == "checklist":
        r = _run(sc, args=["--checklist"])
        if r.stdout:
            print(r.stdout)
        return r.returncode
    if args.action == "list":
        r = _run(sc, args=["--list"])
        if r.stdout:
            print(r.stdout)
        return r.returncode
    print("用法:")
    print("  bidhunter.py compliance scan <文件> [--mode tender|bid|both] [--json] [--llm]")
    print("  bidhunter.py compliance checklist    # 交标前自查清单（31条）")
    print("  bidhunter.py compliance list         # 全部法定红线")
    print("")
    print("  --mode tender = 扫招标文件找埋雷；bid = 扫投标文件找致命项")
    print("  --llm = 附加 LLM 智能补充扫描（需配置 MiniMax Key，会消耗余额）")
    return 1


def cmd_quote(args):
    """v2.7 报价闸门：算式不过禁止出金额（纯本地，零依赖零联网）"""
    extra = list(args.rest or [])
    if args.selftest:
        extra.insert(0, "--selftest")
    if not extra or extra[0] in ("-h", "--help-usage"):
        print("用法:")
        print("  bidhunter.py quote params [--show]   # 首次填一次参数库（最低工资/毛利红线/容差）")
        print("  bidhunter.py quote check --help      # 跑闸门（C-1 地板价 / C2 规模换算 /")
        print("                                       #          C3 单价 / M1 毛利红线）")
        print("  bidhunter.py quote --selftest        # 内置自检")
        print("")
        print("铁律：任一道不过即禁止输出结论金额；缺参数时只交框架与待补清单。")
        return 0
    r = _run("quote_gate.py", args=extra)
    if r.stdout:
        print(r.stdout)
    return r.returncode


def cmd_feedback(args):
    """零成本反馈：本地格式化 -> 剪贴板 -> 打开平台评论页（无后端、无云服务）"""
    extra = []
    if args.platform:
        extra += ["--platform", args.platform]
    if args.no_open:
        extra.append("--no-open")
    if args.type:
        extra += ["--type", args.type]
    if args.scenario:
        extra += ["--scenario", args.scenario]
    if args.detail:
        extra += ["--detail", args.detail]
    r = _run("feedback.py", args=extra)
    return r.returncode


def cmd_help(args):
    print(__doc__)
    return 0


def main():
    p = argparse.ArgumentParser(prog="bidhunter", description="标讯猎手 统一入口")
    sub = p.add_subparsers(dest="cmd")

    sp = sub.add_parser("run"); sp.add_argument("--fresh", action="store_true"); sp.add_argument("--summary", action="store_true"); sp.set_defaults(func=cmd_run)
    sub.add_parser("status").set_defaults(func=cmd_status)
    sub.add_parser("doctor").set_defaults(func=cmd_doctor)
    pd = sub.add_parser("demo"); pd.add_argument("--calendar", action="store_true"); pd.set_defaults(func=cmd_demo)
    pini = sub.add_parser("init", help="首次运行引导：三问生成配置（行业自由输入）")
    pini.add_argument("--preview", action="store_true", help="只预览不写盘")
    pini.set_defaults(func=cmd_init)
    ppaste = sub.add_parser("paste", help="零配置：丢一份招标文件直接出废标风险报告")
    ppaste.add_argument("file", nargs="?")
    ppaste.add_argument("--mode", choices=["tender", "bid", "both"], default="both")
    ppaste.add_argument("--json", action="store_true")
    ppaste.set_defaults(func=cmd_paste)
    pusage = sub.add_parser("usage", help="本地埋点统计（仅写本地，绝不外传）")
    pusage.add_argument("--funnel", action="store_true", help="只看漏斗转化率")
    pusage.set_defaults(func=cmd_usage)
    pc = sub.add_parser("calendar"); pc.add_argument("--days", type=int, default=7); pc.set_defaults(func=cmd_calendar)
    pf = sub.add_parser("faq"); pf.add_argument("terms", nargs="*"); pf.set_defaults(func=cmd_faq)
    pr = sub.add_parser("rules"); pr.add_argument("action", nargs="?"); pr.add_argument("--port", type=int, default=8080); pr.set_defaults(func=cmd_rules)
    pa = sub.add_parser("ai"); pa.add_argument("action", nargs="?"); pa.add_argument("file", nargs="?"); pa.set_defaults(func=cmd_ai)
    pap = sub.add_parser("api"); pap.add_argument("action", nargs="?"); pap.add_argument("--port", type=int, default=8765); pap.set_defaults(func=cmd_api)
    pcomp = sub.add_parser("compliance"); pcomp.add_argument("action", nargs="?"); pcomp.add_argument("file", nargs="?")
    pcomp.add_argument("--mode", default="both", choices=["tender", "bid", "both"])
    pcomp.add_argument("--json", action="store_true"); pcomp.add_argument("--llm", action="store_true")
    pcomp.set_defaults(func=cmd_compliance)
    pgap = sub.add_parser("gap", help="v2.8 待补材料清单 + 零响应检测（纯本地零 API）")
    pgap.add_argument("action", nargs="?", help="scan=待补材料清单 / zero=零响应检测")
    pgap.add_argument("file", nargs="?")
    pgap.add_argument("--json", action="store_true")
    pgap.add_argument("--our-project", help="我方本项目名，用于跨项目残留比对")
    pgap.add_argument("--other-projects", nargs="*", help="其它项目名，用于残留比对")
    pgap.set_defaults(func=cmd_gap)
    psc = sub.add_parser("score", help="v2.9 评分点台账 + 正向覆盖矩阵（纯本地）")
    psc.add_argument("action", nargs="?", help="ledger | coverage | both | selftest")
    psc.add_argument("file", nargs="?")
    psc.add_argument("--json", action="store_true")
    psc.add_argument("--csv", help="CSV 输出路径")
    psc.add_argument("--xlsx", help="xlsx 输出路径（无 openpyxl 则降级 CSV）")
    psc.add_argument("--from-json", help="复用已抽好的 clauses JSON")
    psc.add_argument("--materials", help="材料库文件")
    psc.add_argument("--response", help="投标文件草稿（B2 判 A/B/C 依据）")
    psc.add_argument("--prev-ledger", help="上一版台账 JSON（检测状态回退 A3）")
    psc.add_argument("--deadline", help="投标截止日 YYYY-MM-DD")
    psc.add_argument("--confirm-regress", action="store_true")
    psc.set_defaults(func=cmd_score)
    pq = sub.add_parser("quote", help="报价闸门：算式不过禁止出金额（纯本地）")
    pq.add_argument("--selftest", action="store_true", help="内置自检")
    pq.add_argument("rest", nargs=argparse.REMAINDER)
    pq.set_defaults(func=cmd_quote)
    pfb = sub.add_parser("feedback", help="发送反馈到社区（零成本，无后端）")
    pfb.add_argument("--platform", choices=["skillhub", "clawhub"], default="skillhub")
    pfb.add_argument("--no-open", action="store_true", help="只生成文本，不打开浏览器")
    pfb.add_argument("--type", help="反馈类型编号 0-5（非交互直填）")
    pfb.add_argument("--scenario", help="使用场景（非交互直填）")
    pfb.add_argument("--detail", help="具体描述（非交互直填）")
    pfb.set_defaults(func=cmd_feedback)
    sub.add_parser("help").set_defaults(func=cmd_help)

    if len(sys.argv) < 2:
        cmd_help(None)
        return 0
    args = p.parse_args()
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
