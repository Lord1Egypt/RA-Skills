#!/usr/bin/env python3
"""forge_pipeline.py — S0–S9 工作流硬化（P1-6）。

把「该做哪一步、这一步过没过」从人脑下沉为程序，确定性判定：
  python scripts/forge_pipeline.py --status [--path <技能目录>]   # 列出各阶段闸门状态
  python scripts/forge_pipeline.py --next   [--path <技能目录>]   # 下一步该做哪个阶段
  python scripts/forge_pipeline.py --stage S6 [--path <技能目录>]  # 单独跑某阶段闸门

设计原则：能复用现有确定性工具的，绝不重写——S6 直接调 `forge-publish.py --check`，
S0/S2/S3/S4/S7/S8 走产物存在性判定，S5 走风险分档签批判定。任一阶段不过即当场暴露，不往后续推。
"""
import argparse
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SCRIPTS = os.path.join(HERE)  # 本脚本与同类脚本同目录

STAGES = ["S0", "S1", "S2", "S3", "S4", "S5", "S6", "S7", "S8", "S9"]
STAGE_TITLE = {
    "S0": "脚手架 + 信号注入",
    "S1": "真实接线",
    "S2": "真机取证",
    "S3": "外部标杆（全球）",
    "S4": "覆盖审计",
    "S5": "生产签批（按风险分档）",
    "S6": "校验打包 + 安全审查",
    "S7": "内嵌清晰化闸门",
    "S8": "可推广闸门",
    "S9": "全量自测 + 发布 + 联合测试",
}


def resolve_skill_dir(args):
    if args.path:
        p = os.path.abspath(os.path.expanduser(args.path))
        return p if os.path.isdir(p) else None
    cwd = os.getcwd()
    return cwd if os.path.exists(os.path.join(cwd, "SKILL.md")) else None


def _run(cmd, cwd=None):
    try:
        r = subprocess.run(cmd, cwd=cwd or HERE, capture_output=True, text=True, timeout=120)
        return r.returncode, r.stdout + r.stderr
    except Exception as e:  # noqa
        return 1, str(e)


def check_S0(sd):
    """脚手架 + 信号套件注入完成。"""
    md = os.path.join(sd, "SKILL.md")
    if not os.path.exists(md):
        return False, "缺 SKILL.md"
    text = open(md, encoding="utf-8").read()
    miss = []
    for h in ("## A.0 明确不做清单", "## A.1 交互指令响应", "## A.2 会话钩子"):
        if h not in text:
            miss.append(h)
    if miss:
        return False, f"SKILL.md 缺信号段: {miss}"
    if not os.path.exists(os.path.join(sd, "references", "coverage.md")):
        return False, "缺 references/coverage.md（S0 应自动播种）"
    # KIT 套件存在性
    for rel in ("scripts/upload_signals.py", "scripts/signal_control.py",
                "scripts/download_signals.py", "scripts/session_hook.py",
                "scripts/forge-register.py", "references/signals.md"):
        if not os.path.exists(os.path.join(sd, rel)):
            return False, f"缺信号套件件: {rel}"
    return True, "脚手架 + 信号套件齐备"


def check_S1(sd):
    """真实接线：SKILL.md 含真实调用语法（非占位）。"""
    md = os.path.join(sd, "SKILL.md")
    text = open(md, encoding="utf-8").read() if os.path.exists(md) else ""
    if "scripts/" not in text and "depends" not in text.lower():
        return False, "未检测到真实调用语法（scripts/ 或 depends）"
    return True, "检测到真实调用语法"


def check_S2(sd):
    """真机取证：存在 *_evidence.md。"""
    ref = os.path.join(sd, "references")
    if not os.path.isdir(ref):
        return False, "缺 references/ 目录"
    ev = [f for f in os.listdir(ref) if f.endswith("_evidence.md")]
    if not ev:
        return False, "缺 *_evidence.md（S2 真机取证产物）"
    return True, f"存在 {len(ev)} 个 *_evidence.md"


def check_S3(sd):
    """外部标杆：存在 benchmark.md。"""
    p = os.path.join(sd, "references", "benchmark.md")
    if not os.path.exists(p):
        return False, "缺 references/benchmark.md（S3 全球标杆产物）"
    return True, "存在 benchmark.md"


def check_S4(sd):
    """覆盖审计：coverage.md 含 ✅ 或存在 gap-backlog.md。"""
    cov = os.path.join(sd, "references", "coverage.md")
    if os.path.exists(cov):
        t = open(cov, encoding="utf-8").read()
        if "✅" in t or "✔" in t:
            return True, "coverage.md 已标注覆盖维度"
    if os.path.exists(os.path.join(sd, "references", "gap-backlog.md")):
        return True, "存在 gap-backlog.md"
    return False, "coverage.md 未标注维度且缺 gap-backlog.md"


def check_S5(sd):
    """生产签批：低风险默认过；高风险需 .signoff.md（评审 + 签批）。"""
    # 风险分档：frontmatter 或 SKILL.md 含 risk:high / 高风险 才要求签批
    md = os.path.join(sd, "SKILL.md")
    text = open(md, encoding="utf-8").read() if os.path.exists(md) else ""
    is_high = ("risk" in text.lower() and "high" in text.lower()) or "高风险" in text
    if not is_high:
        return True, "低风险技能：发布前一句确认即可（无需评审文档）"
    signoff = os.path.join(sd, ".signoff.md")
    if not os.path.exists(signoff):
        return False, "高风险技能：缺 .signoff.md（评审文档 + 用户明确签批）"
    return True, "高风险技能：.signoff.md 签批已具"


def check_S6(sd):
    """校验打包 + 安全审查：复用 forge-publish.py --check（含打包干净/闭环/冒烟/注册/S8）。"""
    code, out = _run([sys.executable, os.path.join(SCRIPTS, "forge-publish.py"),
                      "--check", "--path", sd])
    if code != 0:
        # 提取关键失败行
        lines = [l for l in out.splitlines() if "✗" in l or "阻断" in l or "未通过" in l]
        return False, "forge-publish --check 未通过: " + ("; ".join(lines[:3]) or "见输出")
    return True, "forge-publish --check 全绿"


def check_S7(sd):
    """内嵌清晰化闸门：存在清晰化产物（clarity-* 或 SKILL.md 含清晰化标记）。"""
    ref = os.path.join(sd, "references")
    clarity = [f for f in os.listdir(ref)] if os.path.isdir(ref) else []
    if any("clarity" in f.lower() for f in clarity):
        return True, "存在清晰化产物"
    md = os.path.join(sd, "SKILL.md")
    if os.path.exists(md) and "清晰化" in open(md, encoding="utf-8").read():
        return True, "SKILL.md 含清晰化标记"
    return False, "缺清晰化产物（S7 闸门未跑）"


def check_S8(sd):
    """可推广闸门：references/discovery.md + references/intro.md(≤1024) + references/security-audit.md Benign。"""
    refs = os.path.join(sd, "references")
    d = os.path.join(refs, "discovery.md")
    intro = os.path.join(refs, "intro.md")
    sec = os.path.join(refs, "security-audit.md")
    if not os.path.exists(d):
        return False, "缺 references/discovery.md"
    if not os.path.exists(intro):
        return False, "缺 references/intro.md"
    if os.path.exists(intro) and len(open(intro, encoding="utf-8").read()) > 1024:
        return False, "intro.md 超 1024 字符（跨平台介绍上限）"
    if not os.path.exists(sec):
        return False, "缺 references/security-audit.md"
    t = open(sec, encoding="utf-8").read().lower()
    if "benign" not in t and "良性" not in t:
        return False, "security-audit.md 结论非 Benign（云鼎审计未过）"
    return True, "S8 分发就绪（discovery/intro≤1024/security Benign）"


def check_S9(sd):
    """全量自测 + 联合测试：selfcheck 全绿 + joint_test --with-cloud 通过。"""
    sc = os.path.join(SCRIPTS, "selfcheck.py")
    if os.path.exists(sc):
        code, out = _run([sys.executable, sc], cwd=sd)
        if code != 0:
            return False, "selfcheck.py 未全绿（见输出）"
    jt = os.path.join(SCRIPTS, "joint_test.py")
    if os.path.exists(jt):
        code, out = _run([sys.executable, jt, "--with-cloud"], cwd=sd)
        if code != 0:
            return False, "joint_test --with-cloud 未通过（三侧三方不一致）"
    return True, "selfcheck + joint_test 全绿"


CHECKS = {
    "S0": check_S0, "S1": check_S1, "S2": check_S2, "S3": check_S3, "S4": check_S4,
    "S5": check_S5, "S6": check_S6, "S7": check_S7, "S8": check_S8, "S9": check_S9,
}


def main():
    ap = argparse.ArgumentParser(description="S0–S9 工作流硬化闸门")
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--status", action="store_true", help="列出各阶段闸门状态")
    g.add_argument("--next", action="store_true", help="下一步该做哪个阶段")
    g.add_argument("--stage", choices=STAGES, help="单独跑某阶段闸门")
    ap.add_argument("--path", help="技能目录（默认当前目录）")
    args = ap.parse_args()

    sd = resolve_skill_dir(args)
    if not sd:
        print("✗ 未定位技能目录（--path 或当前目录需含 SKILL.md）")
        return 2

    if args.stage:
        ok, msg = CHECKS[args.stage](sd)
        print(f"[{'✓' if ok else '✗'}] {args.stage} {STAGE_TITLE[args.stage]}: {msg}")
        return 0 if ok else 1

    if args.next:
        for s in STAGES:
            ok, msg = CHECKS[s](sd)
            if not ok:
                print(f"→ 下一步做 {s} {STAGE_TITLE[s]}：{msg}")
                return 0
        print("→ 全部阶段已通过，可发布（S9 后执行 forge-publish.py --platform both）")
        return 0

    if args.status:
        print(f"技能目录: {sd}\n{'='*60}")
        all_ok = True
        for s in STAGES:
            ok, msg = CHECKS[s](sd)
            all_ok = all_ok and ok
            print(f"[{'✓' if ok else '✗'}] {s} {STAGE_TITLE[s]}: {msg}")
        print("=" * 60)
        nxt = next((s for s in STAGES if not CHECKS[s](sd)[0]), None)
        if nxt:
            print(f"下一步: {nxt} {STAGE_TITLE[nxt]}")
        else:
            print("全部通过 → 执行 S9 发布: forge-publish.py --path <dir> --platform both --version X.Y.Z")
        return 0 if all_ok else 1


if __name__ == "__main__":
    sys.exit(main())
