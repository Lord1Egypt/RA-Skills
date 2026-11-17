#!/usr/bin/env python3
"""技能锻造炉 · 全量自测入口（selfcheck.py）—— 所有功能一个细节都不遗漏。

聚合本技能全部本地测试为一条命令，输出统一格式（✅/❌ + 计数 + 退出码）：
  1. 结构规范：writing_gate 目录模式（W1–W8）+ changelog 正反例（W9）
  2. 已有测试套件：test_capture_skill_edits.py + test_apply_guard.py（子进程）
  3. 脚本入口健康：全部 scripts/*.py 至少能打印用法/帮助（无崩溃、无 AttributeError）
  4. 关键文件与配置：signals.md / coverage.md / cloud_config.json（4 端点）存在且完整
  5. 本地信号链路：signal_control 四命令 + upload_signals --dry-run + capture --dry-run
     （在临时目录内验证，绝不触碰真实技能内容）

可选 --with-cloud：额外跑云端链路（需凭据/网络，开发侧用，见 cjg-evo/backend/local_test/）。

用法：
  python selfcheck.py              # 本地全量自测（无需网络/凭据）
  python selfcheck.py --verbose    # 显示每个子测试细节
退出码：0=全部通过；2=有失败
"""
import os
import re
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
SKILL_DIR = os.path.dirname(HERE)
PY = sys.executable

VERBOSE = "--verbose" in sys.argv

RESULTS = []


def check(name, cond, detail=""):
    RESULTS.append(cond)
    mark = "✅" if cond else "❌"
    print(f"  {mark} {name}" + (f"  — {detail}" if detail and not cond else ""))
    return cond


def run(cmd, **kw):
    return subprocess.run(cmd, capture_output=True, text=True, **kw)


def section(t):
    print(f"\n== {t} ==", flush=True)


def safe(fn):
    """包裹每个测试段：异常也记录为失败，不让整个自测崩溃（可定位问题）。"""
    try:
        fn()
    except Exception as e:
        import traceback
        RESULTS.append(False)
        print(f"  ❌ 段内异常 {fn.__name__}: {e}", flush=True)
        if VERBOSE:
            traceback.print_exc()


def t1_structure():
    section("① 结构规范（writing_gate W1–W8 + W9 changelog）")
    r = run([PY, os.path.join(HERE, "writing_gate.py"), SKILL_DIR])
    ok = r.returncode == 0
    if VERBOSE or not ok:
        print(r.stdout[-1500:])
    check("W1–W8 + W3a/W3b 写作规范门（目录模式）", ok)

    pos = run([PY, os.path.join(HERE, "writing_gate.py"), "--changelog",
               "v9.9.9：新增「测试功能」，现在可以一键完成；改进「报告」，更清晰。技能文件不会被自动修改。"])
    check("W9 changelog 正例通过", pos.returncode == 0)

    neg = run([PY, os.path.join(HERE, "writing_gate.py"), "--changelog",
               "v9.9.9：Wave B 上线 + L3 聚合 + P1 三指标 + apply_guard.py"])
    check("W9 changelog 反例被拦（生产侧禁词）", neg.returncode == 2)


def t2_existing_suites():
    section("② 已有测试套件")
    for t in ("test_capture_skill_edits.py", "test_apply_guard.py"):
        r = run([PY, os.path.join(HERE, t)])
        passed = len(re.findall(r"✅", r.stdout))
        failed = len(re.findall(r"❌", r.stdout))
        check(f"{t}（{passed}✅ / {failed}❌）", failed == 0 and r.returncode == 0,
              f"exit={r.returncode}")
        if VERBOSE and failed:
            print(r.stdout[-800:])


def t3_script_entries():
    section("③ 全部脚本入口健康（--help/主流程，无崩溃）")
    scripts = sorted(f for f in os.listdir(HERE)
                     if f.endswith(".py") and not f.startswith("test_")
                     and f not in ("selfcheck.py", "joint_test.py"))
    for s in scripts:
        # 各脚本入口探针：--help 优先；无 argparse 的用无参调用（应打印用法而非崩溃）
        r = run([PY, os.path.join(HERE, s), "--help"])
        if r.returncode > 1 and "usage" not in r.stdout.lower() and "用法" not in r.stdout:
            r = run([PY, os.path.join(HERE, s)])
        crash = ("Traceback" in r.stderr) or ("AttributeError" in r.stderr)
        check(f"入口健康 {s}", not crash, f"exit={r.returncode}" + (r.stderr[:120] if crash else ""))
        if VERBOSE and crash:
            print(r.stderr[-600:])


def t4_key_files():
    section("④ 关键文件与配置完整性")
    must = {
        "SKILL.md": os.path.join(SKILL_DIR, "SKILL.md"),
        "references/signals.md": os.path.join(SKILL_DIR, "references", "signals.md"),
        "references/coverage.md": os.path.join(SKILL_DIR, "references", "coverage.md"),
        "references/skill-writing-guide.md": os.path.join(SKILL_DIR, "references", "skill-writing-guide.md"),
        "cloud_config.json": os.path.join(SKILL_DIR, "cloud_config.json"),
    }
    for name, p in must.items():
        check(f"文件存在 {name}", os.path.exists(p))
    cc = os.path.join(SKILL_DIR, "cloud_config.json")
    if os.path.exists(cc):
        try:
            import json
            cfg = json.load(open(cc, encoding="utf-8"))
            need = {"ingest_url", "register_url", "proposal_url", "aggregate_url"}
            missing = need - set(cfg)
            check("cloud_config.json 含 4 个端点 URL", not missing, f"缺 {missing}")
        except Exception as e:
            check("cloud_config.json 可解析", False, str(e))
    # version 单一真相源
    md = open(os.path.join(SKILL_DIR, "SKILL.md"), encoding="utf-8").read()
    m = re.search(r"^version:\s*([\d.]+)", md, re.M)
    pj = os.path.join(SKILL_DIR, ".claude-plugin", "plugin.json")
    v_pj = None
    if os.path.exists(pj):
        try:
            import json
            v_pj = json.load(open(pj, encoding="utf-8")).get("version")
        except Exception:
            pass
    check("版本单一真相源（SKILL.md=plugin.json）",
          m is not None and (v_pj is None or v_pj == m.group(1)),
          f"SKILL.md={m.group(1) if m else '无'} plugin.json={v_pj}")

    # A.0 云进化引导（创建技能时对创作者的强制引导，位于"快速上手"第 0 步，防重构丢失）
    a0 = all(k in md for k in ("云进化引导", "第 0 步", "forge-register.py register", "开启云同步"))
    check("SKILL.md 含 A.0 云进化引导（快速上手第 0 步：注册/云同步/闭环三件套）", a0)

    # A.1/A.2 交互执行强制（交互点不失效：指令响应表 + 会话钩子/收尾信号块）
    a1 = all(k in md for k in ("A.1 交互指令响应", "signal_control.py view", "download_signals.py pull"))
    a2 = all(k in md for k in ("A.2 会话钩子", "收尾信号块", "signals-log.jsonl", "apply_guard.py --snapshot",
                               "session_hook.py start", "session_hook.py end --event"))
    check("SKILL.md 含 A.1 交互指令响应表（9 类指令强制执行）", a1)
    check("SKILL.md 含 A.2 会话钩子（开始补传/拉回 + 收尾信号块 + apply 前瞻）", a2)

    # 发布前校验（随包发布器 --check，本地无网络；含触发词 SEO 校验）
    r = run([PY, os.path.join(HERE, "forge-publish.py"), "--path", SKILL_DIR, "--check"])
    check("forge-publish --check 发布前校验（含 SEO）",
          r.returncode == 0 and "校验通过" in r.stdout, r.stdout[-200:])

    # P1-3 注册状态闸门（防重构丢失：发布校验必须含注册状态段）
    fp = open(os.path.join(HERE, "forge-publish.py"), encoding="utf-8").read()
    check("forge-publish 含注册状态检查段（P1-3 跨会话持久化闸门）",
          "注册状态（跨会话持久化" in fp and "--require-register" in fp)
    # P0-3 锻造炉产物识别闸门（防重构丢失：footer/coverage.md 缺信号套件必阻断）
    check("forge-publish 含锻造炉产物识别闸门（P0-3：缺信号套件必阻断）",
          "锻造炉产物" in fp and "_is_forge_product" in fp)


def t5_local_signal_chain():
    section("⑤ 本地信号链路（临时目录内，零污染真实技能）")
    tmp = tempfile.mkdtemp(prefix="sf-selfcheck-")
    try:
        skill = os.path.join(tmp, "test-skill")
        os.makedirs(os.path.join(skill, "references"))
        # 最小 SKILL.md（writing_gate 结构门需要）
        open(os.path.join(skill, "SKILL.md"), "w", encoding="utf-8").write(
            "---\nname: test-skill\nversion: 9.9.9\ndescription: 'Use when testing selfcheck'\n---\n\n# Test Skill\n\n## 何时使用\n| 场景 | 触发 |\n|------|------|\n| 测试 | test |\n\n## 红线\n- 测试红线\n")
        for f in ("cloud_config.json",):
            open(os.path.join(skill, f), "w", encoding="utf-8").write(
                open(os.path.join(SKILL_DIR, f), encoding="utf-8").read())
        for f in ("signals.md", "coverage.md"):
            p = os.path.join(SKILL_DIR, "references", f)
            if os.path.exists(p):
                open(os.path.join(skill, "references", f), "w", encoding="utf-8").write(
                    open(p, encoding="utf-8").read())
        # 构造一条合法信号
        import uuid
        sig = {
            "ts": "2026-08-22T10:00:00", "signal_id": str(uuid.uuid4()),
            "client_signal_id": str(uuid.uuid4()), "skill_slug": "test-skill",
            "skill_version": "9.9.9", "method_layer": "L3", "event": "helpful",
            "weight": 2, "note": "selfcheck", "anon_id": str(uuid.uuid4()),
        }
        log = os.path.join(skill, "signals-log.jsonl")
        open(log, "a", encoding="utf-8").write(
            __import__("json").dumps(sig, ensure_ascii=False) + "\n")

        # signal_control 四命令
        for c in ("view", "status", "export"):
            r = run([PY, os.path.join(HERE, "signal_control.py"), c, "--dir", skill])
            check(f"signal_control {c}", r.returncode == 0 and "Traceback" not in r.stderr)

        # 显式开启云同步（on），dry-run 统计应见 1 条待传（dry-run 不真正上传）
        open(os.path.join(skill, ".cloud_optin"), "w", encoding="utf-8").write("on")
        r = run([PY, os.path.join(HERE, "upload_signals.py"), "--base", tmp, "--dry-run"])
        check("upload_signals --dry-run 统计待传（on 技能）",
              r.returncode == 0 and "本应上传 1 条" in r.stdout, r.stdout[-200:])
        # bootstrap 语义：缺失才建，已存在不覆盖；新技能默认 .cloud_optin=off
        cloud = open(os.path.join(skill, ".cloud_optin"), encoding="utf-8").read().strip()
        check("bootstrap 不覆盖已存在 .cloud_optin（显式开启保持 on）", cloud == "on", cloud)

        # capture --dry-run（只 diff 不写信号）
        r = run([PY, os.path.join(HERE, "capture_skill_edits.py"), "--skill", "test-skill",
                 "--base", tmp, "--dry-run"])
        check("capture_skill_edits 入口正常（首跑建基线）", r.returncode == 0
              and "Traceback" not in r.stderr, r.stdout[-200:])

        # growth_report 本地（无崩溃，含 ts 时区容错——修复前会 TypeError）
        r = run([PY, os.path.join(HERE, "growth_report.py"), "report", "--dir", skill])
        check("growth_report 本地报告（naive ts 容错）",
              r.returncode == 0 and "Traceback" not in r.stderr and "贡献了 1 条" in r.stdout,
              r.stderr[-200:] + r.stdout[-200:])

        # writing_gate 对任意目录可运行不崩溃（规范 8/8 由 t1 对真实技能验证；此处只测入口健壮性）
        r = run([PY, os.path.join(HERE, "writing_gate.py"), skill])
        check("writing_gate 可对任意目录运行（不崩溃）",
              r.returncode in (0, 2) and "Traceback" not in r.stderr, r.stdout[-200:])

        # G4/G4b session_hook 命令中心：start 首跑不记 → signal 写语义 → start 未收尾记 no_signoff
        # → end --event 写收尾+标记 → start 已收尾不重复记（放末尾避免影响上方"1 条"断言）
        r = run([PY, os.path.join(HERE, "session_hook.py"), "start", "--dir", skill])
        n0 = open(os.path.join(skill, "signals-log.jsonl"), encoding="utf-8").read().count("no_signoff")
        check("session_hook start 首跑（仅建状态不记）", r.returncode == 0 and n0 == 0, r.stdout[-150:])
        r = run([PY, os.path.join(HERE, "session_hook.py"), "signal", "L3:helpful", "--dir", skill])
        check("session_hook signal 写语义信号", r.returncode == 0 and "L3·helpful" in r.stdout, r.stdout[-150:])
        r = run([PY, os.path.join(HERE, "session_hook.py"), "start", "--dir", skill])
        n1 = open(os.path.join(skill, "signals-log.jsonl"), encoding="utf-8").read().count("no_signoff")
        check("session_hook 未收尾再 start → 记 L0·no_signoff", r.returncode == 0 and n1 == 1,
              r.stdout[-150:])
        r = run([PY, os.path.join(HERE, "session_hook.py"), "end", "--event", "L3:suggestion", "--dir", skill])
        n_e = open(os.path.join(skill, "signals-log.jsonl"), encoding="utf-8").read().count("suggestion")
        check("session_hook end --event 写收尾信号+标记", r.returncode == 0 and n_e >= 1, r.stdout[-150:])
        r = run([PY, os.path.join(HERE, "session_hook.py"), "usage", "--calls", "2", "--success", "1",
                 "--errors", "timeout=1", "--dir", skill])
        check("session_hook usage 写客观信号", r.returncode == 0 and "usage_call" in r.stdout, r.stdout[-150:])
        r = run([PY, os.path.join(HERE, "session_hook.py"), "start", "--dir", skill])
        n2 = open(os.path.join(skill, "signals-log.jsonl"), encoding="utf-8").read().count("no_signoff")
        check("session_hook 已收尾再 start → 不重复记", r.returncode == 0 and n2 == 1,
              r.stdout[-150:])
    finally:
        import shutil
        shutil.rmtree(tmp, ignore_errors=True)


def main():
    print(f"技能锻造炉 · 全量自测（skill-forge · {SKILL_DIR}）", flush=True)
    safe(t1_structure)
    safe(t2_existing_suites)
    safe(t3_script_entries)
    safe(t4_key_files)
    safe(t5_local_signal_chain)
    passed = sum(1 for r in RESULTS if r)
    print(f"\nSelfcheck: {passed}/{len(RESULTS)} 通过", flush=True)
    sys.exit(0 if passed == len(RESULTS) else 2)


if __name__ == "__main__":
    main()
