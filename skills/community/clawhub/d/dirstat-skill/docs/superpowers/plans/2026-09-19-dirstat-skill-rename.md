# DirStat_Skill Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Align the public repository identity to `DirStat_Skill`, remove legacy cleanup-oriented wording, and enforce read-only suggestion-only behavior with hard-fail runtime guardrails.

**Architecture:** Keep the existing scan/report pipeline, but rename the public and internal identities so the tool reads as a disk-analysis skill instead of a cleanup advisor. Add explicit platform/engine/path validation in the CLI, reinforce read-only disclaimers in all public entrypoints, and realign the OpenClaw symlink to the new canonical skill path.

**Tech Stack:** Python, argparse CLI, existing tests with pytest, Markdown docs, OpenClaw skill symlinks on DGX.

---

### Task 1: Rename Public Identity And Package

**Files:**
- Create: `Z:\Repositories\DirStat_Skill\docs\superpowers\specs\2026-09-19-dirstat-skill-rename-design.md`
- Modify: `Z:\Repositories\DirStat_Skill\pyproject.toml`
- Modify: `Z:\Repositories\DirStat_Skill\AGENTS.md`
- Modify: `Z:\Repositories\DirStat_Skill\README.md`
- Modify: `Z:\Repositories\DirStat_Skill\src\dirstat_skill\__init__.py`
- Rename: `Z:\Repositories\DirStat_Skill\skills\DirStat_Skill\SKILL.md` -> `Z:\Repositories\DirStat_Skill\skills\DirStat_Skill\SKILL.md`
- Rename: `Z:\Repositories\DirStat_Skill\src\dirstat_skill` -> `Z:\Repositories\DirStat_Skill\src\dirstat_skill`
- Test: `Z:\Repositories\DirStat_Skill\tests\test_cli.py`

- [ ] **Step 1: Write the rename design note**

```md
# DirStat_Skill Rename Design

- public identity becomes `DirStat_Skill`
- package identity becomes `dirstat_skill`
- all public wording becomes read-only suggestion-only
- old cleanup wording is removed from repo entrypoints
```

- [ ] **Step 2: Run a search to map rename scope**

Run: a repo-wide string search for the previous identity, legacy bucket labels, and old dossier filenames.
Expected: multiple matches across docs, package imports, tests, and OpenClaw helper scripts.

- [ ] **Step 3: Apply the public/package rename**

```toml
[project]
name = "DirStat_Skill"
description = "Read-only disk usage analysis skill that suggests what to review without removing anything"
```

```python
__all__ = [
    "__version__",
]
```

- [ ] **Step 4: Rename directories and imports**

```bash
Move-Item Z:\Repositories\DirStat_Skill\src\dirstat_skill Z:\Repositories\DirStat_Skill\src\dirstat_skill
Move-Item Z:\Repositories\DirStat_Skill\skills\DirStat_Skill Z:\Repositories\DirStat_Skill\skills\DirStat_Skill
```

- [ ] **Step 5: Update tests for the new package and CLI identity**

```python
from dirstat_skill.cli import main
```

- [ ] **Step 6: Commit**

```bash
git add pyproject.toml AGENTS.md README.md src skills tests docs/superpowers/specs/2026-09-19-dirstat-skill-rename-design.md
git commit -m "refactor: rename public skill identity to DirStat_Skill"
```

### Task 2: Enforce Read-Only Suggestion-Only Language

**Files:**
- Modify: `Z:\Repositories\DirStat_Skill\README.md`
- Modify: `Z:\Repositories\DirStat_Skill\AGENTS.md`
- Modify: `Z:\Repositories\DirStat_Skill\skills\DirStat_Skill\SKILL.md`
- Modify: `Z:\Repositories\DirStat_Skill\src\dirstat_skill\reporting.py`
- Test: `Z:\Repositories\DirStat_Skill\tests\test_reporting.py`

- [ ] **Step 1: Add the opening disclaimer to all public entrypoints**

```md
> READ-ONLY ANALYSIS ONLY
> This skill never removes files, never schedules cleanup, and never performs cleanup actions.
> It only scans, summarizes, and suggests what a human should review.
```

- [ ] **Step 2: Replace legacy bucket labels with review-oriented labels**

```python
BUCKET_LABELS = {
    "review_first": "review first",
    "review_carefully": "review carefully",
    "keep_protected": "keep protected",
}
```

- [ ] **Step 3: Update the dossier rendering to use suggestion wording**

```md
- recommended_review_action
- why_reviewed
- dependency_check
```

- [ ] **Step 4: Add a reporting test for non-destructive language**

```python
def test_report_uses_review_only_language() -> None:
    report = render_review_report("C:\\", candidates)
    assert "remove" not in report.lower()
    assert "review first" in report.lower()
```

- [ ] **Step 5: Commit**

```bash
git add README.md AGENTS.md skills/DirStat_Skill/SKILL.md src/dirstat_skill/reporting.py tests/test_reporting.py
git commit -m "docs: reinforce read-only review-only contract"
```

### Task 3: Add Hard-Fail Runtime Guardrails

**Files:**
- Modify: `Z:\Repositories\DirStat_Skill\src\dirstat_skill\cli.py`
- Modify: `Z:\Repositories\DirStat_Skill\src\dirstat_skill\targets.py`
- Test: `Z:\Repositories\DirStat_Skill\tests\test_cli.py`

- [ ] **Step 1: Write failing tests for invalid engine/platform/path combinations**

```python
def test_windows_native_fails_on_linux() -> None:
    with pytest.raises(ValueError, match="windows-native can run only on Windows"):
        main(["audit", "--path", "C:\\", "--engine", "windows-native", "--output-dir", "out", "--config", "config/defaults.json"])


def test_ncdu_fails_for_windows_style_path() -> None:
    with pytest.raises(ValueError, match="Windows-style paths require the Windows runtime"):
        main(["audit", "--path", "C:\\", "--engine", "ncdu", "--output-dir", "out", "--config", "config/defaults.json"])
```

- [ ] **Step 2: Run the targeted test to confirm failure**

Run: `pytest tests/test_cli.py -k "windows_native_fails_on_linux or ncdu_fails_for_windows_style_path" -v`
Expected: FAIL because the current CLI accepts these combinations.

- [ ] **Step 3: Implement the validation helpers**

```python
def _validate_runtime_contract(engine_name: str, paths: list[str]) -> None:
    system_name = platform.system().lower()
    has_windows_path = any(":\\" in path or path.startswith("\\\\") for path in paths)
    has_linux_path = any(path.startswith("/") for path in paths)
    if engine_name == "windows-native" and system_name != "windows":
        raise ValueError("windows-native can run only on Windows. Run the scan on a Windows host and summarize elsewhere if needed.")
    if engine_name == "ncdu" and has_windows_path:
        raise ValueError("Windows-style paths require the Windows runtime. Run DirStat_Skill on Windows for that target.")
    if system_name == "windows" and engine_name == "ncdu":
        raise ValueError("ncdu is a Linux engine. Run DirStat_Skill on Linux or use the Windows runtime on Windows.")
    if system_name == "windows" and has_linux_path:
        raise ValueError("Linux-style paths require a Linux runtime.")
```

- [ ] **Step 4: Call the guardrail before target normalization**

```python
engine_name = _resolve_engine_name(settings, requested_engine)
_validate_runtime_contract(engine_name=engine_name, paths=paths)
```

- [ ] **Step 5: Re-run the targeted test**

Run: `pytest tests/test_cli.py -k "windows_native_fails_on_linux or ncdu_fails_for_windows_style_path" -v`
Expected: PASS

- [ ] **Step 6: Commit**

```bash
git add src/dirstat_skill/cli.py tests/test_cli.py
git commit -m "fix: hard-fail invalid runtime and path combinations"
```

### Task 4: Update OpenClaw Integration And Final Verification

**Files:**
- Modify: `Z:\Repositories\DirStat_Skill\trash\relink_openclaw_skill_to_repo.sh`
- Modify: `Z:\Repositories\DirStat_Skill\trash\install_openclaw_skill.py`
- Modify: `Z:\Repositories\DirStat_Skill\.agent\HANDOFF.md`
- Test: `Z:\Repositories\DirStat_Skill\tests\test_cli.py`
- Test: `Z:\Repositories\DirStat_Skill\tests\test_reporting.py`

- [ ] **Step 1: Update helper scripts to the new `DirStat_Skill` path**

```bash
/home/jagones/Repositories/DirStat_Skill/skills/DirStat_Skill
```

- [ ] **Step 2: Update OpenClaw symlink targets**

```bash
/home/jagones/.openclaw/workspace/skills/DirStat_Skill -> /home/jagones/Repositories/DirStat_Skill/skills/DirStat_Skill
/home/jagones/.openclaw/skills/DirStat_Skill -> /home/jagones/.openclaw/workspace/skills/DirStat_Skill
```

- [ ] **Step 3: Run the focused Python test suite**

Run: `pytest tests/test_cli.py tests/test_reporting.py tests/test_config.py tests/test_targets.py -v`
Expected: PASS

- [ ] **Step 4: Run a final string search for forbidden legacy wording**

Run: a repo-wide string search for the previous identity, old bucket labels, and old dossier filenames.
Expected: only intentional migration-history notes remain; no active public entrypoint or runtime string uses the old wording.

- [ ] **Step 5: Update `.agent/HANDOFF.md` with the new canonical identity and guardrails**

```md
- canonical public identity: `DirStat_Skill`
- canonical package: `dirstat_skill`
- contract: read-only analysis and suggestion only
- guardrails: runtime hard-fails on invalid engine/platform/path combinations
```

- [ ] **Step 6: Commit**

```bash
git add trash .agent/HANDOFF.md tests
git commit -m "chore: realign OpenClaw integration to DirStat_Skill"
```

