#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
变异测试：验证 tests/selfcheck.py 真的「能抓出问题」，而不是一枚橡皮图章。
做法：在 /tmp 的技能副本上逐个注入已知缺陷，运行 selfcheck，期望其报错。
若注入缺陷后 selfcheck 仍全绿，说明该项检查无效。
"""
import os, re, shutil, subprocess, sys, json, pathlib

# 路径自适应：技能根目录由脚本位置推导，工作副本与输出均置于 out/ 下
import pathlib as _pl
_HERE = _pl.Path(__file__).resolve().parent
SRC = str(_HERE.parent)
WORK = os.environ.get("V7_MUT_WORK") or str(_HERE / "out" / "mut-skill")
SELF = os.path.join(WORK, "tests", "selfcheck.py")

MUTATIONS = [
    ("身份数表述滞后：八重 → 四重", "SKILL.md",
     lambda t: t.replace("## 角色定位（八重专业身份）", "## 角色定位（四重专业身份）")),
    ("门控维数表述滞后：14 → 13", "SKILL.md",
     lambda t: t.replace("| **14. L4 调度门控（V7.0 新增 ⭐）**",
                         "| **13. L4 调度门控（V7.0 新增 ⭐）**")),
    ("运营流数表述滞后：六类 → 四类", "SKILL.md",
     lambda t: t.replace("六类运营流 OPS-1~6", "四类运营流 OPS-1~6")),
    ("meta.json icon 退回空串", "meta.json",
     lambda t: t.replace('"author": "AI Literacy Expert"',
                         '"icon": "",\n  "author": "AI Literacy Expert"')),
    ("版本号篡改：7.0.0 → 6.0.0", "meta.json",
     lambda t: t.replace('"version": "7.0.0"', '"version": "6.0.0"')),
    ("状态缓存路径退回硬编码 /workspace", "assets/automation-registry.json",
     lambda t: t.replace('"<宿主工作目录>/.ai-literacy-state/<TASK_ID>.json"',
                         '"/workspace/.ai-literacy-state/<TASK_ID>.json"')),
    ("硬编码安装目录 /root/.codebuddy", "references/workflow-orchestrator.md",
     lambda t: t + "\n\n见 /root/.codebuddy/skills/ai-literacy-expert-v5/SKILL.md\n"),
    ("悬空引用", "SKILL.md",
     lambda t: t + "\n\n详见 `references/this-file-does-not-exist.md`\n"),
    ("删除 tests 脚本（可验证性丢失）", "tests/t2-idempotent-sim.py", None),  # 特殊：删除
    ("指令模板缺失【幂等】段", "assets/self-contained-prompt-template.md",
     lambda t: t.replace("【幂等】", "【重复检查】")),
    ("cron 秒位非 0（违规秒级）", "references/automation-ops.md",
     lambda t: t.replace("--cron \"0 0 8 * * 1\"", "--cron \"30 0 8 * * 1\"", 1)),
    ("敏感信息泄露", "references/automation-l4-scheduler.md",
     lambda t: t + '\n\napi_key: "REDACTED-SECRET"\n'),
    ("QA 项数声明滞后：14 → 16（README）", "README.md",
     lambda t: t.replace("**14 项 QA 门控**", "**16 项 QA 门控**")),
    ("QA 项数声明滞后：14 → 16（SKILL.md 第 8 维）", "SKILL.md",
     lambda t: t.replace("| 8. QA 全量验收门控 | 14 项标准 QA 清单",
                         "| 8. QA 全量验收门控 | 16 项标准 QA 清单")),
    ("QA 清册计数未随清单更新（删 1 条仍称 14 项）",
     "references/commercial-production-standards.md",
     lambda t: t.replace("- 用户操作门槛（教师无需编程经验即可使用）✅\n", "")),
]


def run_selfcheck():
    env = dict(os.environ, V7_TEST_OUT="/tmp/mut-out")
    p = subprocess.run([sys.executable, SELF, "--quiet"],
                       capture_output=True, text=True, env=env, cwd=WORK)
    return p.returncode, p.stdout + p.stderr


print("=" * 78)
print("变异测试：注入缺陷 → 期望 selfcheck 报错（returncode=1）")
print("=" * 78)

# 基线：未变异时必须全绿
shutil.rmtree(WORK, ignore_errors=True)
shutil.copytree(SRC, WORK, ignore=shutil.ignore_patterns("out", "__pycache__"))
rc, out = run_selfcheck()
print(f"\n[基线] 未注入缺陷 → rc={rc}（期望 0）")
if rc != 0:
    print(out[-1500:])
    print("❌ 基线就不通过，无法继续变异测试")
    sys.exit(1)
print("  ✅ 基线通过\n")

caught, missed = [], []
for i, (desc, rel, fn) in enumerate(MUTATIONS, 1):
    shutil.rmtree(WORK, ignore_errors=True)
    shutil.copytree(SRC, WORK, ignore=shutil.ignore_patterns("out", "__pycache__"))
    target = os.path.join(WORK, rel)
    if fn is None:                       # 删除型变异
        os.remove(target)
    else:
        txt = open(target, encoding="utf-8").read()
        new = fn(txt)
        if new == txt:
            print(f"  ⚠️  [{i:02d}] {desc} —— 变异未生效（原文未匹配），跳过")
            continue
        open(target, "w", encoding="utf-8").write(new)
    rc, out = run_selfcheck()
    tag = "✅ 已捕获" if rc != 0 else "❌ 漏检"
    (caught if rc != 0 else missed).append(desc)
    print(f"  {tag}  [{i:02d}] {desc}")
    if rc == 0:
        print("       ↳ selfcheck 仍然全绿，该项检查无效！")
    else:
        # 打印它抓到的失败项，确认抓的是同一个问题
        for line in out.splitlines():
            if line.startswith("  - ["):
                print("       ↳ " + line.strip()[:110])
                break

print("\n" + "=" * 78)
print(f"  捕获 {len(caught)}/{len(caught) + len(missed)}   漏检 {len(missed)}")
if missed:
    print("  漏检项：")
    for m in missed:
        print("    -", m)
print("=" * 78)
sys.exit(1 if missed else 0)
