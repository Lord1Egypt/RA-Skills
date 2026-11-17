# DirStat_Skill v2 Cross-Platform Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Turn the repository into one public, read-only disk-audit skill that works on Windows and Linux, including ARM64 DGX, with one CLI and one output contract.

**Architecture:** Keep the normalized data model and reporting pipeline, but refactor scan execution behind platform-specific engine adapters. Add a native Windows engine built on Python 3.12 stdlib, preserve the Linux `ncdu` engine, and expose both through a generic `scan` / `summarize-export` / `audit` CLI.

**Tech Stack:** Python 3.12 stdlib (`argparse`, `dataclasses`, `json`, `logging`, `os`, `pathlib`, `shutil`, `platform`), `pytest`, Bash for Linux helpers, PowerShell only for verification commands

---

## File Structure

- Create: `Z:\Repositories\DirStat_Skill\src\dirstat_skill\engine_base.py`
  - shared engine protocol, target dataclasses, raw export metadata
- Create: `Z:\Repositories\DirStat_Skill\src\dirstat_skill\engine_windows.py`
  - native Windows scanner using `os.scandir()` and `shutil.disk_usage()`
- Create: `Z:\Repositories\DirStat_Skill\src\dirstat_skill\targets.py`
  - target parsing, drive discovery, path validation
- Create: `Z:\Repositories\DirStat_Skill\src\dirstat_skill\logging_utils.py`
  - structured per-run log formatting and file logger setup
- Create: `Z:\Repositories\DirStat_Skill\src\dirstat_skill\raw_export.py`
  - raw export loading and engine dispatch for normalization
- Create: `Z:\Repositories\DirStat_Skill\tests\test_targets.py`
  - path and platform target tests
- Create: `Z:\Repositories\DirStat_Skill\tests\test_engine_windows.py`
  - Windows engine unit tests
- Create: `Z:\Repositories\DirStat_Skill\tests\fixtures\windows_tree_export.json`
  - small Windows raw export fixture
- Create: `Z:\Repositories\DirStat_Skill\tests\fixtures\linux_generic_export.json`
  - small generic raw export fixture if needed by shared loader tests
- Modify: `Z:\Repositories\DirStat_Skill\src\dirstat_skill\models.py`
  - add cross-platform raw export metadata and normalized scan result types
- Modify: `Z:\Repositories\DirStat_Skill\src\dirstat_skill\engine_ncdu.py`
  - adapt current Linux engine to shared engine interface
- Modify: `Z:\Repositories\DirStat_Skill\src\dirstat_skill\ncdu_json.py`
  - integrate shared raw export loader path
- Modify: `Z:\Repositories\DirStat_Skill\src\dirstat_skill\risk.py`
  - split platform-aware safety rules
- Modify: `Z:\Repositories\DirStat_Skill\src\dirstat_skill\reporting.py`
  - keep output contract stable while accepting generic raw metadata
- Modify: `Z:\Repositories\DirStat_Skill\src\dirstat_skill\config.py`
  - extend settings for engine and platform rule configuration
- Modify: `Z:\Repositories\DirStat_Skill\src\dirstat_skill\cli.py`
  - replace Linux-only CLI with `scan`, `summarize-export`, `audit`
- Modify: `Z:\Repositories\DirStat_Skill\config\defaults.json`
  - add Windows danger zones and shared defaults
- Modify: `Z:\Repositories\DirStat_Skill\tests\test_config.py`
- Modify: `Z:\Repositories\DirStat_Skill\tests\test_engine_ncdu.py`
- Modify: `Z:\Repositories\DirStat_Skill\tests\test_reporting.py`
- Modify: `Z:\Repositories\DirStat_Skill\tests\test_cli.py`
- Modify: `Z:\Repositories\DirStat_Skill\README.md`
  - rewrite as global Windows+Linux repo
- Modify: `Z:\Repositories\DirStat_Skill\AGENTS.md`
  - point agents to generic workflow
- Modify: `Z:\Repositories\DirStat_Skill\skills\DirStat_Skill\SKILL.md`
  - generic skill workflow for Windows and Linux
- Move: `Z:\Repositories\DirStat_Skill\scripts\dgx\*.sh` -> `Z:\Repositories\DirStat_Skill\scripts\linux\*.sh`
  - keep Linux helpers but stop branding them as DGX-only

### Task 1: Introduce Shared Engine And Target Abstractions

**Files:**
- Create: `Z:\Repositories\DirStat_Skill\src\dirstat_skill\engine_base.py`
- Create: `Z:\Repositories\DirStat_Skill\src\dirstat_skill\targets.py`
- Create: `Z:\Repositories\DirStat_Skill\tests\test_targets.py`
- Modify: `Z:\Repositories\DirStat_Skill\src\dirstat_skill\models.py`
- Modify: `Z:\Repositories\DirStat_Skill\src\dirstat_skill\config.py`
- Modify: `Z:\Repositories\DirStat_Skill\tests\test_config.py`

- [ ] **Step 1: Write the failing target tests**

```python
from pathlib import Path

import pytest

from dirstat_skill.targets import ScanTarget, normalize_targets


def test_normalize_targets_keeps_multiple_explicit_paths() -> None:
    targets = normalize_targets(
        requested_paths=["C:\\", "D:\\models", "F:\\"],
        auto_discover=False,
        platform_name="windows",
    )

    assert targets == [
        ScanTarget(raw_path="C:\\", resolved_path=Path("C:/"), platform_name="windows"),
        ScanTarget(raw_path="D:\\models", resolved_path=Path("D:/models"), platform_name="windows"),
        ScanTarget(raw_path="F:\\", resolved_path=Path("F:/"), platform_name="windows"),
    ]


def test_normalize_targets_rejects_empty_request_when_auto_discover_disabled() -> None:
    with pytest.raises(ValueError, match="No scan targets were provided"):
        normalize_targets(requested_paths=[], auto_discover=False, platform_name="windows")
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python -m pytest tests/test_targets.py -v`
Expected: FAIL with `ModuleNotFoundError` or missing symbol errors for `dirstat_skill.targets`

- [ ] **Step 3: Write minimal shared abstractions**

```python
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class ScanTarget:
    raw_path: str
    resolved_path: Path
    platform_name: str


def normalize_targets(
    requested_paths: list[str],
    auto_discover: bool,
    platform_name: str,
) -> list[ScanTarget]:
    if not requested_paths and not auto_discover:
        raise ValueError("No scan targets were provided")

    normalized: list[ScanTarget] = []
    for raw_path in requested_paths:
        normalized.append(
            ScanTarget(
                raw_path=raw_path,
                resolved_path=Path(raw_path),
                platform_name=platform_name,
            )
        )
    return normalized
```

- [ ] **Step 4: Extend config settings for generic engines**

```python
@dataclass(frozen=True)
class Settings:
    top_n: int
    min_bytes: int
    one_file_system: bool
    exclude_patterns: list[str]
    risk_do_not_touch_prefixes: list[str]
    risk_needs_inspection_prefixes: list[str]
    windows_do_not_touch_prefixes: list[str]
    default_engine_windows: str
    default_engine_linux: str
```

```json
{
  "top_n": 50,
  "min_bytes": 1073741824,
  "one_file_system": true,
  "exclude_patterns": [".cache", "node_modules", "__pycache__"],
  "risk_do_not_touch_prefixes": ["/etc", "/usr", "/boot", "/var/lib"],
  "risk_needs_inspection_prefixes": ["/opt", "/srv", "/var/log", "/var/tmp", "/home"],
  "windows_do_not_touch_prefixes": ["C:\\Windows", "C:\\Program Files", "C:\\Program Files (x86)"],
  "default_engine_windows": "windows-native",
  "default_engine_linux": "ncdu"
}
```

- [ ] **Step 5: Run tests to verify they pass**

Run: `python -m pytest tests/test_targets.py tests/test_config.py -v`
Expected: PASS

- [ ] **Step 6: Commit**

```bash
git add src/dirstat_skill/engine_base.py src/dirstat_skill/targets.py src/dirstat_skill/models.py src/dirstat_skill/config.py config/defaults.json tests/test_targets.py tests/test_config.py
git commit -m "feat: add shared scan target abstractions"
```

### Task 2: Add Native Windows Scan Engine

**Files:**
- Create: `Z:\Repositories\DirStat_Skill\src\dirstat_skill\engine_windows.py`
- Create: `Z:\Repositories\DirStat_Skill\tests\test_engine_windows.py`
- Create: `Z:\Repositories\DirStat_Skill\tests\fixtures\windows_tree_export.json`
- Modify: `Z:\Repositories\DirStat_Skill\src\dirstat_skill\models.py`

- [ ] **Step 1: Write the failing Windows engine tests**

```python
from pathlib import Path

from dirstat_skill.engine_windows import build_windows_export


def test_build_windows_export_writes_raw_json(tmp_path: Path) -> None:
    source_root = tmp_path / "scan-root"
    source_root.mkdir()
    (source_root / "cache.bin").write_bytes(b"x" * 8)
    (source_root / "nested").mkdir()
    (source_root / "nested" / "weights.gguf").write_bytes(b"y" * 16)

    export_path = tmp_path / "windows-export.json"
    result = build_windows_export(target=source_root, output_path=export_path)

    assert result.engine_name == "windows-native"
    assert export_path.exists()
    assert '"path"' in export_path.read_text(encoding="utf-8")
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python -m pytest tests/test_engine_windows.py -v`
Expected: FAIL with `ModuleNotFoundError` for `dirstat_skill.engine_windows`

- [ ] **Step 3: Write minimal Windows engine**

```python
from __future__ import annotations

from dataclasses import dataclass
import json
import os
from pathlib import Path


@dataclass(frozen=True)
class WindowsExportResult:
    engine_name: str
    output_path: Path


def _scan_path(root: Path) -> list[dict[str, object]]:
    nodes: list[dict[str, object]] = []
    with os.scandir(root) as entries:
        for entry in entries:
            entry_path = Path(entry.path)
            if entry.is_dir(follow_symlinks=False):
                nodes.append(
                    {
                        "path": str(entry_path),
                        "name": entry.name,
                        "is_dir": True,
                        "size": 0,
                    }
                )
                nodes.extend(_scan_path(entry_path))
            else:
                nodes.append(
                    {
                        "path": str(entry_path),
                        "name": entry.name,
                        "is_dir": False,
                        "size": entry.stat(follow_symlinks=False).st_size,
                    }
                )
    return nodes


def build_windows_export(target: Path, output_path: Path) -> WindowsExportResult:
    payload = {
        "engine": "windows-native",
        "root": str(target),
        "nodes": _scan_path(target),
    }
    output_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    return WindowsExportResult(engine_name="windows-native", output_path=output_path)
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `python -m pytest tests/test_engine_windows.py -v`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add src/dirstat_skill/engine_windows.py tests/test_engine_windows.py tests/fixtures/windows_tree_export.json src/dirstat_skill/models.py
git commit -m "feat: add native windows scan engine"
```

### Task 3: Refactor Linux `ncdu` Engine Behind Shared Interface

**Files:**
- Modify: `Z:\Repositories\DirStat_Skill\src\dirstat_skill\engine_ncdu.py`
- Modify: `Z:\Repositories\DirStat_Skill\tests\test_engine_ncdu.py`
- Modify: `Z:\Repositories\DirStat_Skill\src\dirstat_skill\ncdu_json.py`
- Create: `Z:\Repositories\DirStat_Skill\src\dirstat_skill\raw_export.py`

- [ ] **Step 1: Write the failing shared raw export loader tests**

```python
from pathlib import Path

from dirstat_skill.raw_export import load_raw_export


def test_load_raw_export_reads_windows_engine_payload() -> None:
    fixture_path = Path("tests/fixtures/windows_tree_export.json")
    payload = load_raw_export(fixture_path)

    assert payload["engine"] == "windows-native"
    assert payload["root"].endswith("scan-root")


def test_load_raw_export_reads_ncdu_payload() -> None:
    fixture_path = Path("tests/fixtures/ncdu_minimal_export.json")
    payload = load_raw_export(fixture_path)

    assert payload["engine"] == "ncdu"
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `python -m pytest tests/test_engine_ncdu.py tests/test_cli.py -v`
Expected: FAIL because `load_raw_export` and shared engine metadata do not exist yet

- [ ] **Step 3: Add shared raw export loading**

```python
from __future__ import annotations

import json
from pathlib import Path


def load_raw_export(export_path: Path) -> dict[str, object]:
    payload = json.loads(export_path.read_text(encoding="utf-8"))
    if isinstance(payload, dict) and "engine" in payload:
        return payload
    return {"engine": "ncdu", "payload": payload}
```

- [ ] **Step 4: Adapt `engine_ncdu.py` to return shared metadata**

```python
def build_ncdu_export_command(
    binary: str,
    target: Path,
    output_path: Path,
    one_file_system: bool,
    exclude_patterns: list[str],
) -> list[str]:
    command = [binary]
    if one_file_system:
        command.append("-x")
    command.extend(["-o", output_path.as_posix()])
    for pattern in exclude_patterns:
        command.extend(["--exclude", pattern])
    command.append(target.as_posix())
    return command
```

- [ ] **Step 5: Run tests to verify they pass**

Run: `python -m pytest tests/test_engine_ncdu.py tests/test_cli.py -v`
Expected: PASS

- [ ] **Step 6: Commit**

```bash
git add src/dirstat_skill/raw_export.py src/dirstat_skill/engine_ncdu.py src/dirstat_skill/ncdu_json.py tests/test_engine_ncdu.py tests/test_cli.py
git commit -m "refactor: unify linux raw export handling"
```

### Task 4: Replace Linux-Only CLI With Generic `scan`, `summarize-export`, And `audit`

**Files:**
- Modify: `Z:\Repositories\DirStat_Skill\src\dirstat_skill\cli.py`
- Modify: `Z:\Repositories\DirStat_Skill\src\dirstat_skill\reporting.py`
- Create: `Z:\Repositories\DirStat_Skill\src\dirstat_skill\logging_utils.py`
- Modify: `Z:\Repositories\DirStat_Skill\tests\test_cli.py`
- Modify: `Z:\Repositories\DirStat_Skill\tests\test_reporting.py`

- [ ] **Step 1: Write the failing CLI tests**

```python
import subprocess
import sys
from pathlib import Path


def test_cli_audit_command_writes_summary_bundle(tmp_path: Path) -> None:
    target_root = tmp_path / "audit-root"
    target_root.mkdir()
    (target_root / "blob.bin").write_bytes(b"x" * 32)

    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "dirstat_skill.cli",
            "audit",
            "--path",
            str(target_root),
            "--output-dir",
            str(tmp_path / "run"),
            "--engine",
            "windows-native",
        ],
        text=True,
        capture_output=True,
        check=False,
    )

    assert result.returncode == 0
    assert (tmp_path / "run" / "summary.md").exists()
    assert (tmp_path / "run" / "candidates.json").exists()
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python -m pytest tests/test_cli.py -v`
Expected: FAIL because the CLI only supports `summarize-export`

- [ ] **Step 3: Write minimal generic CLI structure**

```python
parser = argparse.ArgumentParser(prog="DirStat_Skill")
subparsers = parser.add_subparsers(dest="command", required=True)

scan_parser = subparsers.add_parser("scan")
scan_parser.add_argument("--path", action="append", dest="paths", required=True)
scan_parser.add_argument("--output-dir", required=True)
scan_parser.add_argument("--engine", default=None)

summarize_parser = subparsers.add_parser("summarize-export")
summarize_parser.add_argument("--export", required=True)
summarize_parser.add_argument("--output-dir", required=True)
summarize_parser.add_argument("--config", required=True)

audit_parser = subparsers.add_parser("audit")
audit_parser.add_argument("--path", action="append", dest="paths", required=True)
audit_parser.add_argument("--output-dir", required=True)
audit_parser.add_argument("--engine", default=None)
audit_parser.add_argument("--config", default="config/defaults.json")
```

- [ ] **Step 4: Add structured run logging**

```python
import logging
from pathlib import Path


def configure_run_logger(log_path: Path) -> logging.Logger:
    logger = logging.getLogger("dirstat_skill")
    logger.handlers.clear()
    logger.setLevel(logging.INFO)

    handler = logging.FileHandler(log_path, encoding="utf-8")
    handler.setFormatter(logging.Formatter("[%(levelname)s] | %(asctime)s | %(name)s | %(message)s"))
    logger.addHandler(handler)
    return logger
```

- [ ] **Step 5: Run tests to verify they pass**

Run: `python -m pytest tests/test_cli.py tests/test_reporting.py -v`
Expected: PASS

- [ ] **Step 6: Commit**

```bash
git add src/dirstat_skill/cli.py src/dirstat_skill/reporting.py src/dirstat_skill/logging_utils.py tests/test_cli.py tests/test_reporting.py
git commit -m "feat: add generic scan and audit cli"
```

### Task 5: Add Cross-Platform Risk Rules And Keep Output Contract Stable

**Files:**
- Modify: `Z:\Repositories\DirStat_Skill\src\dirstat_skill\risk.py`
- Modify: `Z:\Repositories\DirStat_Skill\tests\test_risk.py`
- Modify: `Z:\Repositories\DirStat_Skill\src\dirstat_skill\reporting.py`

- [ ] **Step 1: Write the failing risk tests**

```python
from dirstat_skill.risk import classify_path


def test_classify_path_marks_windows_system_paths_as_keep_protected() -> None:
    assert classify_path(
        path="C:\\Windows\\System32",
        keep_protected_prefixes=["C:\\Windows", "C:\\Program Files"],
        review_carefully_prefixes=["C:\\Users"],
    ) == "keep protected"


def test_classify_path_marks_windows_user_cache_as_review_first() -> None:
    assert classify_path(
        path="C:\\Users\\giova\\AppData\\Local\\Temp\\huge.tmp",
        keep_protected_prefixes=["C:\\Windows", "C:\\Program Files"],
        review_carefully_prefixes=["C:\\Users"],
    ) == "review first"
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python -m pytest tests/test_risk.py -v`
Expected: FAIL because Windows-specific buckets are not recognized yet

- [ ] **Step 3: Extend risk logic**

```python
def classify_path(
    path: str,
    keep_protected_prefixes: list[str],
    review_carefully_prefixes: list[str],
) -> str:
    lowered = path.lower()
    if any(lowered.startswith(prefix.lower()) for prefix in keep_protected_prefixes):
        return "keep protected"
    if "\\appdata\\local\\temp\\" in lowered or lowered.endswith(".filepart"):
        return "review first"
    if any(lowered.startswith(prefix.lower()) for prefix in review_carefully_prefixes):
        return "review carefully"
    return "review first"
```

- [ ] **Step 4: Verify the report writer still emits the same public files**

Run: `python -m pytest tests/test_risk.py tests/test_reporting.py -v`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add src/dirstat_skill/risk.py src/dirstat_skill/reporting.py tests/test_risk.py tests/test_reporting.py
git commit -m "feat: add cross-platform risk classification"
```

### Task 6: Move Linux Helper Scripts And Rewrite Public Docs

**Files:**
- Move: `Z:\Repositories\DirStat_Skill\scripts\dgx\verify_ncdu.sh` -> `Z:\Repositories\DirStat_Skill\scripts\linux\verify_ncdu.sh`
- Move: `Z:\Repositories\DirStat_Skill\scripts\dgx\install_ncdu.sh` -> `Z:\Repositories\DirStat_Skill\scripts\linux\install_ncdu.sh`
- Move: `Z:\Repositories\DirStat_Skill\scripts\dgx\run_audit.sh` -> `Z:\Repositories\DirStat_Skill\scripts\linux\run_audit.sh`
- Move: `Z:\Repositories\DirStat_Skill\scripts\dgx\show_latest_audit.sh` -> `Z:\Repositories\DirStat_Skill\scripts\linux\show_latest_audit.sh`
- Move: `Z:\Repositories\DirStat_Skill\scripts\dgx\find_safe_candidates.sh` -> `Z:\Repositories\DirStat_Skill\scripts\linux\find_safe_candidates.sh`
- Move: `Z:\Repositories\DirStat_Skill\scripts\dgx\prepare_linux_scripts.sh` -> `Z:\Repositories\DirStat_Skill\scripts\linux\prepare_linux_scripts.sh`
- Modify: `Z:\Repositories\DirStat_Skill\README.md`
- Modify: `Z:\Repositories\DirStat_Skill\AGENTS.md`
- Modify: `Z:\Repositories\DirStat_Skill\skills\DirStat_Skill\SKILL.md`
- Modify: `Z:\Repositories\DirStat_Skill\.gitignore`

- [ ] **Step 1: Write the failing documentation checks**

```python
from pathlib import Path


def test_readme_mentions_windows_and_linux() -> None:
    readme = Path("README.md").read_text(encoding="utf-8")
    assert "Windows" in readme
    assert "Linux" in readme
    assert "DGX/Linux-first" not in readme


def test_skill_points_to_generic_commands() -> None:
    skill_text = Path("skills/DirStat_Skill/SKILL.md").read_text(encoding="utf-8")
    assert "scripts/linux/" in skill_text
    assert "audit --path" in skill_text
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python -m pytest tests/test_cli.py -v`
Expected: FAIL because docs still describe a Linux-first workflow and `scripts/dgx/*`

- [ ] **Step 3: Rewrite public docs and pointers**

```markdown
## Supported Platforms

- Windows: native Python scanner, local drives or explicit paths
- Linux: `ncdu` engine plus generic CLI

## Example Commands

- Windows: `python -m dirstat_skill.cli audit --path C:\ --output-dir outputs\sample`
- Linux: `python3 -m dirstat_skill.cli audit --path /home --engine ncdu --output-dir outputs/sample`
```

```markdown
## Repository Entry Points

- `README.md`
- `AGENTS.md`
- `skills/DirStat_Skill/SKILL.md`
- `scripts/linux/*.sh` for Linux-only helpers
```

- [ ] **Step 4: Run docs and smoke tests**

Run: `python -m pytest tests/test_cli.py -v`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add scripts/linux README.md AGENTS.md skills/DirStat_Skill/SKILL.md .gitignore
git commit -m "docs: publish one cross-platform skill workflow"
```

### Task 7: Verify On Windows And Linux ARM64

**Files:**
- Modify: `Z:\Repositories\DirStat_Skill\README.md`
  - add verified commands and observed behavior
- Modify: `Z:\Repositories\DirStat_Skill\skills\DirStat_Skill\SKILL.md`
  - update quick reference after real verification

- [ ] **Step 1: Run the full local test suite**

Run: `python -m pytest tests -v`
Expected: PASS

- [ ] **Step 2: Run Windows verification on at least one local system drive**

Run: `python -m dirstat_skill.cli audit --path C:\ --output-dir outputs\win_c_audit`
Expected:
- `outputs\win_c_audit\summary.md`
- `outputs\win_c_audit\top_dirs.csv`
- `outputs\win_c_audit\top_files.csv`
- `outputs\win_c_audit\candidates.json`
- `outputs\win_c_audit\run.log`

- [ ] **Step 3: Run Windows verification on a second volume if available**

Run: `python -m dirstat_skill.cli audit --path D:\ --output-dir outputs\win_d_audit`
Expected: same output bundle as Step 2

- [ ] **Step 4: Run Linux helper verification on DGX**

Run: `ssh dgx bash /home/jagones/Repositories/DirStat_Skill/scripts/linux/prepare_linux_scripts.sh`
Expected: `prepared_linux_scripts=yes`

- [ ] **Step 5: Run Linux audit verification on DGX**

Run: `ssh dgx /home/jagones/Repositories/DirStat_Skill/scripts/linux/run_audit.sh`
Expected: a new dated output folder plus compact report bundle

- [ ] **Step 6: Update README and SKILL with real verified commands and paths**

```markdown
- Verified on Windows: `C:\`, `D:\` if available
- Verified on Linux ARM64: DGX via `ncdu`
- Output contract confirmed on both platforms
```

- [ ] **Step 7: Commit**

```bash
git add README.md skills/DirStat_Skill/SKILL.md
git commit -m "test: verify cross-platform audit workflow"
```

## Self-Review

### Spec coverage

- generic engine abstraction: Task 1
- Windows native scanner: Task 2
- Linux preservation: Task 3 and Task 7
- generic CLI refactor: Task 4
- cross-platform risk rules: Task 5
- documentation rewrite: Task 6
- Windows and Linux verification: Task 7

No spec requirement is left without a task.

### Placeholder scan

- no `TBD`
- no `TODO`
- no “implement later”
- every code-changing step includes code or exact commands

### Type consistency

- `ScanTarget` defined in Task 1 and reused consistently
- engine names fixed as `windows-native` and `ncdu`
- CLI commands fixed as `scan`, `summarize-export`, and `audit`
- public Python package remains `dirstat_skill`

