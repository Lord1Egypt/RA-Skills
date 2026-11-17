#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""cjg-skill-sync 本地自检（离线，不联网、不碰真实技能目录）。

项目纪律 18：新能力必须自带 selfcheck。本脚本用临时沙箱验证：
版本比较、更新分级、本地改动检测、备份/回滚、默认配置守铁律。

跑法：python scripts/selfcheck.py
"""
import os
import sys
import json
import shutil
import tempfile

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import skill_sync as S  # noqa: E402

SKILL_DIR = os.path.dirname(HERE)
FAILS = []


def check(name, cond, extra=""):
    print(("  ✅ " if cond else "  ❌ ") + name + ((" | " + str(extra))[:200] if extra else ""))
    if not cond:
        FAILS.append(name)


def make_fake_skill(root, slug, version, files=None):
    d = os.path.join(root, slug)
    os.makedirs(d, exist_ok=True)
    open(os.path.join(d, "SKILL.md"), "w", encoding="utf-8").write(
        "---\nslug: %s\nname: %s\ndisplayName: %s\nversion: %s\n"
        "description: test\nagent_created: true\n---\n\n# t\n" % (slug, slug, slug, version))
    for fn, content in (files or {"a.txt": "hello"}).items():
        p = os.path.join(d, fn)
        # 支持 "sub/b.txt" 这类嵌套路径（首版漏了 makedirs，自检已抓到）
        os.makedirs(os.path.dirname(p), exist_ok=True)
        open(p, "w", encoding="utf-8").write(content)
    return d


print("=== 1) 目录结构 ===")
for rel in ("SKILL.md", "scripts/skill_sync.py", "config.json"):
    check(f"存在 {rel}", os.path.exists(os.path.join(SKILL_DIR, rel)))

print("\n=== 2) SKILL.md frontmatter 必填字段 ===")
meta = S.parse_frontmatter(os.path.join(SKILL_DIR, "SKILL.md"))
for k in ("slug", "name", "displayName", "version", "description", "agent_created"):
    check(f"字段 {k}", bool(meta.get(k)), meta.get(k, "")[:40])

print("\n=== 3) 语义化版本比较（非字符串比较） ===")
check("1.10.0 > 1.9.1", S.vkey("1.10.0") > S.vkey("1.9.1"))
check("3.1.0 > 3.0.4", S.vkey("3.1.0") > S.vkey("3.0.4"))
check("1.0.0 == 1.0", S.vkey("1.0.0") == S.vkey("1.0"))

print("\n=== 4) 更新分级 ===")
check("1.9.1→2.0.0 = major", S.classify("1.9.1", "2.0.0") == "major")
check("3.0.4→3.1.0 = minor", S.classify("3.0.4", "3.1.0") == "minor")
check("3.0.4→3.0.5 = patch", S.classify("3.0.4", "3.0.5") == "patch")
check("3.0.4→3.0.4 = latest", S.classify("3.0.4", "3.0.4") == "latest")

print("\n=== 5) 默认配置守铁律（不改机器） ===")
cfg = S.load_config()
check("auto_check_enabled 默认 False", cfg.get("auto_check_enabled") is False, cfg.get("auto_check_enabled"))
check("auto_apply_safe_only 默认 True", cfg.get("auto_apply_safe_only") is True)
check("skill_version_url 已配置", bool(cfg.get("skill_version_url")))

print("\n=== 6) 沙箱：扫描 + 本地改动检测 + 备份回滚 ===")
tmp = tempfile.mkdtemp(prefix="cjg_sync_selfcheck_")
root = os.path.join(tmp, "skills")
os.makedirs(root)
d = make_fake_skill(root, "demo-skill", "1.0.0", {"a.txt": "hello", "sub/b.txt": "world"})

orig_dirs, S.SKILLS_DIRS = S.SKILLS_DIRS, [root]
try:
    found = S.scan_installed()
    check("扫描到 demo-skill", "demo-skill" in found, list(found))
    check("版本解析 1.0.0", found.get("demo-skill", {}).get("version") == "1.0.0")

    state, _ = S.check_local_changes(d)
    check("无快照时 = unknown（最保守）", state == "unknown", state)

    S.write_baseline(d)
    state, _ = S.check_local_changes(d)
    check("建快照后 = clean", state == "clean", state)

    open(os.path.join(d, "a.txt"), "w", encoding="utf-8").write("I CHANGED IT")
    state, changed = S.check_local_changes(d)
    check("改动后 = modified", state == "modified", state)
    check("定位到改动文件 a.txt", "a.txt" in changed, changed)

    # 备份 → 破坏 → 回滚 → 内容复原
    bak = S.backup_dir(d, "demo-skill")
    check("备份目录存在", os.path.isdir(bak))
    open(os.path.join(d, "a.txt"), "w", encoding="utf-8").write("BROKEN")
    ok = S.restore_dir(d, bak)
    restored = open(os.path.join(d, "a.txt"), encoding="utf-8").read()
    check("回滚成功且内容复原", ok and restored == "I CHANGED IT", restored)
    check("回滚保留 .cjg_sync", os.path.isdir(os.path.join(d, S.SYNC_META)))
finally:
    S.SKILLS_DIRS = orig_dirs
    shutil.rmtree(tmp, ignore_errors=True)

print("\n=== 7) 离线可用性（不联网也能检查） ===")
try:
    import subprocess
    r = subprocess.run([sys.executable, os.path.join(HERE, "skill_sync.py"),
                        "check", "--offline", "--no-baseline"],
                       capture_output=True, text=True, timeout=60,
                       cwd=os.path.dirname(SKILL_DIR))
    check("check --offline 退出码 0", r.returncode == 0, r.stderr[-160:])
    check("输出含表头", "技能更新检查" in (r.stdout or ""), (r.stdout or "")[:60])
except Exception as e:
    check("check --offline 可运行", False, f"{type(e).__name__}: {str(e)[:120]}")

print("\n=== 8) autorun 守门（默认关 = 不改机器） ===")
try:
    import subprocess
    exe = [sys.executable, os.path.join(HERE, "skill_sync.py")]
    r0 = subprocess.run(exe + ["autorun", "--help"], capture_output=True,
                        text=True, timeout=60)
    check("autorun 子命令已注册", r0.returncode == 0, r0.stderr[-120:])
    r = subprocess.run(exe + ["autorun"], capture_output=True, text=True,
                       timeout=120, cwd=os.path.dirname(SKILL_DIR))
    check("autorun 退出码 0", r.returncode == 0, r.stderr[-160:])
    out = r.stdout or ""
    check("未开启时直接跳过（不扫描不改动）", "⏭" in out, out[:80])
except Exception as e:
    check("autorun 守门可验证", False, f"{type(e).__name__}: {str(e)[:120]}")

print("\n=== 9) 安装源解析 + 停滞检测（备份外置后不会被安装冲掉） ===")
tmp2 = tempfile.mkdtemp(prefix="cjg_sync_sc2_")
orig_root = S.BACKUP_ROOT
try:
    S.BACKUP_ROOT = os.path.join(tmp2, "backups")
    info = {"install_urls": {"skillhub": "cli:skillhub:demo-skill",
                             "github": "https://github.com/x/y"}}
    items = S.plan_install("demo-skill", info,
                           target_dir=os.path.join(tmp2, "demo-skill"),
                           version="1.1.0")
    plats = [i["plat"] for i in items]
    check("解析出 skillhub + github 两个源",
          "skillhub" in plats and "github" in plats, plats)
    sh = [i for i in items if i["plat"] == "skillhub"][0]
    has_cli = S.cli_available("skillhub")
    check("cli: 前缀按 CLI 可用性判定",
          (sh["auto"] is True) if has_cli else (sh["auto"] is False),
          f"has_cli={has_cli}")
    gh = [i for i in items if i["plat"] == "github"][0]
    check("普通 URL = 手动，绝不自动装", gh["auto"] is False)
    check("初始不判停滞", S.is_stalled("demo-skill", "1.1.0") is False)
    S.mark_stalled("demo-skill", "1.1.0")
    check("标记后同版本判停滞", S.is_stalled("demo-skill", "1.1.0") is True)
    check("出现更高版本则不判停滞", S.is_stalled("demo-skill", "1.2.0") is False)
    check("停滞记录写在技能目录之外",
          os.path.exists(os.path.join(S.BACKUP_ROOT, "stalled.json")))
finally:
    S.BACKUP_ROOT = orig_root
    shutil.rmtree(tmp2, ignore_errors=True)

print("\n" + "=" * 56)
if FAILS:
    print(f"SELFCHECK FAILED ❌ {len(FAILS)} 项 -> " + "; ".join(FAILS))
    sys.exit(1)
print("SELFCHECK ALL PASS ✅")
