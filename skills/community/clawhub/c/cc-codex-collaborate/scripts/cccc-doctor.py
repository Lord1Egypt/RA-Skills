#!/usr/bin/env python3
"""CCCC Doctor — diagnose installation, config, hooks, Codex, gates, and context."""
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(os.environ.get("CLAUDE_PROJECT_DIR", subprocess.getoutput("git rev-parse --show-toplevel 2>/dev/null || pwd")).strip())
SKILL_DIR = ROOT / ".claude/skills/cc-codex-collaborate"
WORKSPACE = ROOT / "docs/cccc"
SETTINGS = ROOT / ".claude/settings.json"

PASS = "PASS"
WARN = "WARN"
FAIL = "FAIL"

results: list[tuple[str, str, str]] = []  # (level, label, detail)
fix_suggestions: list[str] = []


def record(level: str, label: str, detail: str = ""):
    results.append((level, label, detail))
    if level == FAIL:
        fix_suggestions.append(f"FIX: {label}" + (f" — {detail}" if detail else ""))


def read_json(path: Path) -> dict | None:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return None


def lang() -> str:
    cfg = read_json(WORKSPACE / "config.json")
    if cfg:
        return cfg.get("language", {}).get("user_language", "zh")
    return "zh"


def t(zh: str, _en: str = "") -> str:
    return zh if lang() != "en" else (_en or zh)


def check_installation():
    record(PASS, f"Skill directory: {SKILL_DIR.relative_to(ROOT)}" if SKILL_DIR.exists() else "",
           "" if SKILL_DIR.exists() else "missing")
    if not SKILL_DIR.exists():
        record(FAIL, "Skill 未安装", ".claude/skills/cc-codex-collaborate 不存在")
        return False

    for f in ["VERSION", "SKILL.md", "scripts", "templates"]:
        p = SKILL_DIR / f
        if p.exists():
            if f == "VERSION":
                ver = p.read_text().strip()
                record(PASS, f"Skill version: {ver}")
            else:
                record(PASS, f"  {f}/ exists")
        else:
            record(FAIL, f"  {f} missing", f"Skill 不完整: {f}")
    return True


def check_workspace():
    if not WORKSPACE.exists():
        record(FAIL, "docs/cccc 不存在", "运行 /cc-codex-collaborate setup")
        return False
    record(PASS, "docs/cccc/ exists")

    for f in ["config.json", "state.json", "roadmap.md", "milestone-backlog.md", "context-bundle.md"]:
        p = WORKSPACE / f
        if f in ("config.json", "state.json"):
            if p.exists():
                data = read_json(p)
                if data is not None:
                    record(PASS, f"  {f} valid JSON")
                else:
                    record(FAIL, f"  {f} invalid JSON")
            else:
                record(FAIL, f"  {f} missing")
        else:
            if p.exists():
                record(PASS, f"  {f} exists")
            else:
                record(WARN, f"  {f} missing", f"尚未生成 {f}")
    return True


def check_config_state():
    cfg = read_json(WORKSPACE / "config.json")
    st = read_json(WORKSPACE / "state.json")
    if not cfg or not st:
        return

    mode = cfg.get("mode", "unknown")
    loop = cfg.get("automation", {}).get("stop_hook_loop_enabled", False)
    max_cont = cfg.get("automation", {}).get("max_stop_hook_continuations", 10)
    record(PASS if mode in ("supervised-auto", "full-auto-safe", "manual") else WARN,
           f"config.mode = {mode}")
    record(PASS, f"config.stop_hook_loop_enabled = {loop}")
    record(PASS, f"config.max_continuations = {max_cont}")

    status = st.get("status", "UNKNOWN")
    pause = st.get("pause_reason")
    mid = st.get("current_milestone_id")
    cont = st.get("stop_hook_continuations", 0)
    record(PASS, f"state.status = {status}")
    if pause:
        record(WARN, f"state.pause_reason = {pause}")
    else:
        record(PASS, "state.pause_reason = null")
    record(PASS if mid else WARN,
           f"state.current_milestone_id = {mid or '(empty)'}")
    record(PASS, f"state.stop_hook_continuations = {cont}")

    # Deprecated fields check
    if "mode" in st:
        record(WARN, "state.json contains deprecated 'mode' field", "应迁移到 config.json")
    if "enabled" in st:
        record(WARN, "state.json contains deprecated 'enabled' field", "应迁移到 config.json")

    # Mismatch checks
    backlog_path = WORKSPACE / "milestone-backlog.md"
    if not mid and backlog_path.exists():
        text = backlog_path.read_text(encoding="utf-8")
        import re
        in_prog = re.findall(r'(?:M\d+\w*).*?in.progress', text, re.IGNORECASE)
        if in_prog:
            record(WARN, "state.current_milestone_id empty but backlog has in-progress milestone",
                   "运行 /cc-codex-collaborate reset state")

    if mode == "full-auto-safe" and not loop:
        record(WARN, "config.mode is full-auto-safe but loop not enabled")

    if loop and status in ("READY", "IMPLEMENTING", "READY_TO_CONTINUE") and cont >= max_cont:
        record(WARN, f"continuations ({cont}) >= max ({max_cont})", "运行 /cc-codex-collaborate reset state 重置")


def check_hooks():
    if not SETTINGS.exists():
        record(WARN, ".claude/settings.json not found", "hooks 未注册")
        return

    data = read_json(SETTINGS) or {}
    hooks = data.get("hooks", {})
    registered_events = set()
    for event, groups in hooks.items():
        for group in groups:
            for h in group.get("hooks", []):
                cmd = h.get("command", "")
                if "cccc" in cmd.lower():
                    registered_events.add(event)

    hook_scripts = {
        "Stop": "cccc-stop.sh",
        "PreToolUse": "cccc-sensitive-op-guard.sh",
        "StopFailure": "cccc-stop-failure.sh",
    }
    for event, script in hook_scripts.items():
        reg = event in registered_events
        script_path = ROOT / ".claude/hooks" / script
        exists = script_path.exists()
        executable = os.access(script_path, os.X_OK) if exists else False

        if reg:
            record(PASS, f"{event} hook registered")
        else:
            record(WARN, f"{event} hook NOT registered", "运行 /cc-codex-collaborate loop-start")

        if exists:
            record(PASS, f"  {script} exists")
        else:
            record(FAIL, f"  {script} missing", "运行 /cc-codex-collaborate force-update")

        if exists and not executable:
            record(WARN, f"  {script} not executable", "chmod +x")

    # Stop hook simulation
    stop_script = ROOT / ".claude/hooks" / "cccc-stop.sh"
    if stop_script.exists() and os.access(stop_script, os.X_OK):
        try:
            r = subprocess.run(
                ["bash", str(stop_script)],
                input='{"stop_hook_active":false}',
                capture_output=True, text=True, timeout=10,
                env={**os.environ, "CLAUDE_PROJECT_DIR": str(ROOT)},
                cwd=str(ROOT),
            )
            stdout = r.stdout.strip()
            if stdout:
                try:
                    parsed = json.loads(stdout)
                    if parsed.get("decision") == "block":
                        record(PASS, "Stop hook simulation: decision=block")
                    else:
                        record(WARN, f"Stop hook simulation: decision={parsed.get('decision', '?')}")
                except json.JSONDecodeError:
                    record(FAIL, "Stop hook stdout is not valid JSON", f"输出: {stdout[:100]}")
            else:
                record(PASS, "Stop hook simulation: no block (exited)")
        except Exception as e:
            record(WARN, f"Stop hook simulation failed: {e}")


def check_commands():
    cmd_dir = ROOT / ".claude/commands"
    if not cmd_dir.exists():
        record(WARN, ".claude/commands/ not found", "运行 /cc-codex-collaborate force-update")
        return

    expected = ["cc-codex-collaborate.md", "cc-codex-collaborate-loop-start.md",
                "cc-codex-collaborate-loop-status.md", "cc-codex-collaborate-loop-stop.md"]
    for name in expected:
        p = cmd_dir / name
        if not p.exists():
            record(WARN, f"  {name} missing", "运行 /cc-codex-collaborate force-update")
            continue
        record(PASS, f"  {name} exists")
        content = p.read_text(encoding="utf-8")
        if "generated-by:" in content or "generated-file:" in content:
            record(PASS, f"    has generated-by marker")
        else:
            record(WARN, f"    no generated-by marker (user-modified)")

        # Check for hardcoded absolute paths
        import re
        abs_paths = re.findall(r'/Users/[^\s"<\']+|/home/[^\s"<\']+', content)
        if abs_paths:
            record(FAIL, f"    hardcoded absolute path(s): {abs_paths[:3]}", "移除硬编码路径")


def check_codex():
    cfg = read_json(WORKSPACE / "config.json")
    if not cfg:
        return
    codex_cfg = cfg.get("codex", {})
    cli_cmd = codex_cfg.get("cli_command", "codex")

    cli_path = shutil.which(cli_cmd)
    if cli_path:
        record(PASS, f"Codex CLI: {cli_path}")
        try:
            ver = subprocess.run([cli_cmd, "--version"], capture_output=True, text=True, timeout=10)
            if ver.returncode == 0:
                record(PASS, f"  Codex version: {ver.stdout.strip()[:60]}")
            else:
                record(WARN, f"  codex --version failed: exit {ver.returncode}")
        except Exception as e:
            record(WARN, f"  codex --version error: {e}")
    else:
        record(FAIL, f"Codex CLI not found: {cli_cmd}", "安装 Codex CLI 或配置 config.codex.cli_command")

    record(PASS, f"config.codex.required = {codex_cfg.get('required', True)}")
    record(PASS, f"config.codex.fail_closed = {codex_cfg.get('fail_closed', True)}")

    st = read_json(WORKSPACE / "state.json")
    if st:
        for gate_name, key in [("Plan review", "codex_plan_review_status"),
                                ("Final review", "codex_final_review_status"),
                                ("Milestone review", "current_milestone_codex_review_status")]:
            val = st.get(key, "not_run")
            level = PASS if val == "pass" else WARN if val == "not_run" else FAIL
            record(level, f"  {gate_name}: {val}")


def check_context():
    ctx_path = WORKSPACE / "context-bundle.md"
    if not ctx_path.exists():
        record(WARN, "context-bundle.md missing", "运行 /cc-codex-collaborate rebuild-context")
        return
    record(PASS, "context-bundle.md exists")

    text = ctx_path.read_text(encoding="utf-8")
    expected_sections = ["Git status", "Git diff", "Untracked", "milestone-backlog"]
    for section in expected_sections:
        if section.lower() in text.lower():
            record(PASS, f"  contains '{section}' section")
        else:
            record(WARN, f"  missing '{section}' section", "运行 /cc-codex-collaborate rebuild-context")

    # Check staleness: compare with latest git activity
    import datetime
    try:
        ctx_mtime = datetime.datetime.fromtimestamp(ctx_path.stat().st_mtime, tz=datetime.timezone.utc)
        r = subprocess.run(["git", "log", "-1", "--format=%ct"], capture_output=True, text=True, cwd=str(ROOT))
        if r.returncode == 0 and r.stdout.strip():
            git_ts = datetime.datetime.fromtimestamp(int(r.stdout.strip()), tz=datetime.timezone.utc)
            if git_ts > ctx_mtime:
                record(WARN, "context-bundle.md is older than latest git commit", "运行 /cc-codex-collaborate rebuild-context")
            else:
                record(PASS, "context-bundle.md is up-to-date")
    except Exception:
        pass

    # Check for secrets in context
    secret_patterns = ["BEGIN PRIVATE KEY", "BEGIN RSA PRIVATE KEY", "SECRET_KEY", "-----BEGIN CERTIFICATE"]
    for pat in secret_patterns:
        if pat in text:
            record(FAIL, f"context-bundle.md contains secret pattern: {pat}", "立即从 context 中移除！")


def main():
    print("cc-codex-collaborate doctor")
    print()

    check_installation()
    check_workspace()
    check_config_state()
    check_hooks()
    check_commands()
    check_codex()
    check_context()

    # Output results
    fail_count = sum(1 for r in results if r[0] == FAIL)
    warn_count = sum(1 for r in results if r[0] == WARN)
    pass_count = sum(1 for r in results if r[0] == PASS)

    for level, label, detail in results:
        marker = {"PASS": "PASS", "WARN": "WARN", "FAIL": "FAIL"}[level]
        line = f"  {marker:4}  {label}"
        if detail and level != PASS:
            line += f" — {detail}"
        print(line)

    print()
    print(f"Summary: {pass_count} PASS, {warn_count} WARN, {fail_count} FAIL")

    if fix_suggestions:
        print()
        print("建议修复：")
        for i, s in enumerate(fix_suggestions, 1):
            print(f"  {i}. {s}")

    return 1 if fail_count > 0 else 0


if __name__ == "__main__":
    sys.exit(main())
