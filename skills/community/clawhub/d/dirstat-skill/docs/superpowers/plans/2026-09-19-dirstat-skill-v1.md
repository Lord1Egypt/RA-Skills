# DirStat_Skill v1 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a DGX-first, read-only disk audit pipeline that uses system-installed `ncdu`, keeps raw scan data out of the LLM by default, and emits compact risk-ranked reports.

**Architecture:** A Python package provides configuration loading, `ncdu` command construction, JSON export parsing, risk classification, and compact report generation. Thin shell wrappers under `scripts/dgx/` are used only for host-side verification and live runs on the DGX, while all summarization logic remains testable in Python.

**Tech Stack:** Python 3.12, stdlib `argparse`/`json`/`dataclasses`/`pathlib`, `pytest`, Bash for DGX wrappers, system-installed `ncdu`

---

## File Structure

- `Z:\Repositories\DirStat_Skill\pyproject.toml`
  - Python project metadata and `pytest` config
- `Z:\Repositories\DirStat_Skill\config\defaults.json`
  - default thresholds, exclude rules, and risk lists
- `Z:\Repositories\DirStat_Skill\src\dirstat_skill\__init__.py`
  - package marker
- `Z:\Repositories\DirStat_Skill\src\dirstat_skill\config.py`
  - config dataclasses and loader
- `Z:\Repositories\DirStat_Skill\src\dirstat_skill\models.py`
  - normalized node/report dataclasses
- `Z:\Repositories\DirStat_Skill\src\dirstat_skill\engine_ncdu.py`
  - engine detection and command creation
- `Z:\Repositories\DirStat_Skill\src\dirstat_skill\ncdu_json.py`
  - parser for `ncdu -o` JSON exports
- `Z:\Repositories\DirStat_Skill\src\dirstat_skill\risk.py`
  - risk bucket assignment
- `Z:\Repositories\DirStat_Skill\src\dirstat_skill\reporting.py`
  - summary generation and output writers
- `Z:\Repositories\DirStat_Skill\src\dirstat_skill\cli.py`
  - CLI entry point
- `Z:\Repositories\DirStat_Skill\scripts\dgx\verify_ncdu.sh`
  - fail-fast verification of `ncdu` presence on DGX
- `Z:\Repositories\DirStat_Skill\scripts\dgx\install_ncdu.sh`
  - guarded installer that stops if unattended sudo is unavailable
- `Z:\Repositories\DirStat_Skill\scripts\dgx\run_audit.sh`
  - live read-only export launcher
- `Z:\Repositories\DirStat_Skill\tests\fixtures\ncdu_minimal_export.json`
  - fixed sample export for parser tests
- `Z:\Repositories\DirStat_Skill\tests\test_config.py`
  - config loader tests
- `Z:\Repositories\DirStat_Skill\tests\test_engine_ncdu.py`
  - engine command builder tests
- `Z:\Repositories\DirStat_Skill\tests\test_ncdu_json.py`
  - parser tests
- `Z:\Repositories\DirStat_Skill\tests\test_risk.py`
  - risk bucket tests
- `Z:\Repositories\DirStat_Skill\tests\test_reporting.py`
  - summary/report generation tests
- `Z:\Repositories\DirStat_Skill\tests\test_cli.py`
  - CLI smoke tests
- `Z:\Repositories\DirStat_Skill\outputs\.gitkeep`
  - keep tracked empty output root
- `Z:\Repositories\DirStat_Skill\trash\.gitkeep`
  - keep tracked empty scratch root
- `Z:\Repositories\DirStat_Skill\.agent\HANDOFF.md`
  - update status and blockers after live verification
- `Z:\Repositories\DirStat_Skill\README.md`
  - update with real usage commands after implementation

### Task 1: Bootstrap Python Project

**Files:**
- Create: `Z:\Repositories\DirStat_Skill\pyproject.toml`
- Create: `Z:\Repositories\DirStat_Skill\config\defaults.json`
- Create: `Z:\Repositories\DirStat_Skill\src\dirstat_skill\__init__.py`
- Create: `Z:\Repositories\DirStat_Skill\src\dirstat_skill\config.py`
- Create: `Z:\Repositories\DirStat_Skill\tests\test_config.py`
- Create: `Z:\Repositories\DirStat_Skill\outputs\.gitkeep`
- Create: `Z:\Repositories\DirStat_Skill\trash\.gitkeep`

- [ ] **Step 1: Write the failing config test**

```python
from pathlib import Path

from dirstat_skill.config import load_settings


def test_load_settings_reads_defaults_and_overrides(tmp_path: Path) -> None:
    config_path = tmp_path / "defaults.json"
    config_path.write_text(
        """
        {
          "top_n": 20,
          "min_bytes": 1048576,
          "one_file_system": true,
          "exclude_patterns": [".cache", "node_modules"],
          "risk_do_not_touch_prefixes": ["/etc", "/usr", "/var/lib"],
          "risk_needs_inspection_prefixes": ["/opt", "/srv", "/var/log"]
        }
        """.strip(),
        encoding="utf-8",
    )

    settings = load_settings(
        config_path=config_path,
        env_overrides={"TOP_N": "50", "MIN_BYTES": "1073741824"},
    )

    assert settings.top_n == 50
    assert settings.min_bytes == 1073741824
    assert settings.one_file_system is True
    assert settings.exclude_patterns == [".cache", "node_modules"]
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python -m pytest tests/test_config.py -v`
Expected: FAIL with `ModuleNotFoundError: No module named 'dirstat_skill'`

- [ ] **Step 3: Write minimal project bootstrap**

```toml
[build-system]
requires = ["setuptools>=68"]
build-backend = "setuptools.build_meta"

[project]
name = "DirStat_Skill"
version = "0.1.0"
description = "Read-only disk audit pipeline for DGX/Linux hosts"
requires-python = ">=3.12"
dependencies = []

[project.optional-dependencies]
dev = ["pytest>=8.3"]

[tool.pytest.ini_options]
pythonpath = ["src"]
testpaths = ["tests"]
```

```python
from __future__ import annotations

from dataclasses import dataclass
import json
from pathlib import Path


@dataclass(frozen=True)
class Settings:
    top_n: int
    min_bytes: int
    one_file_system: bool
    exclude_patterns: list[str]
    risk_do_not_touch_prefixes: list[str]
    risk_needs_inspection_prefixes: list[str]


def load_settings(config_path: Path, env_overrides: dict[str, str] | None = None) -> Settings:
    payload = json.loads(config_path.read_text(encoding="utf-8"))
    overrides = env_overrides or {}
    return Settings(
        top_n=int(overrides.get("TOP_N", payload["top_n"])),
        min_bytes=int(overrides.get("MIN_BYTES", payload["min_bytes"])),
        one_file_system=bool(payload["one_file_system"]),
        exclude_patterns=list(payload["exclude_patterns"]),
        risk_do_not_touch_prefixes=list(payload["risk_do_not_touch_prefixes"]),
        risk_needs_inspection_prefixes=list(payload["risk_needs_inspection_prefixes"]),
    )
```

```json
{
  "top_n": 50,
  "min_bytes": 1073741824,
  "one_file_system": true,
  "exclude_patterns": [
    ".cache",
    "node_modules",
    "__pycache__"
  ],
  "risk_do_not_touch_prefixes": [
    "/etc",
    "/usr",
    "/boot",
    "/var/lib"
  ],
  "risk_needs_inspection_prefixes": [
    "/opt",
    "/srv",
    "/var/log",
    "/var/tmp",
    "/home"
  ]
}
```

- [ ] **Step 4: Run test to verify it passes**

Run: `python -m pytest tests/test_config.py -v`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add pyproject.toml config/defaults.json src/dirstat_skill/__init__.py src/dirstat_skill/config.py tests/test_config.py outputs/.gitkeep trash/.gitkeep
git commit -m "feat: bootstrap python project and config loader"
```

### Task 2: Add `ncdu` Engine Detection And Command Building

**Files:**
- Create: `Z:\Repositories\DirStat_Skill\src\dirstat_skill\models.py`
- Create: `Z:\Repositories\DirStat_Skill\src\dirstat_skill\engine_ncdu.py`
- Create: `Z:\Repositories\DirStat_Skill\tests\test_engine_ncdu.py`
- Create: `Z:\Repositories\DirStat_Skill\scripts\dgx\verify_ncdu.sh`

- [ ] **Step 1: Write the failing engine tests**

```python
from pathlib import Path

from dirstat_skill.engine_ncdu import build_ncdu_export_command, detect_ncdu


def test_detect_ncdu_returns_none_when_binary_missing() -> None:
    assert detect_ncdu(path_entries=[]) is None


def test_build_ncdu_export_command_uses_json_export_and_one_filesystem(tmp_path: Path) -> None:
    output_path = tmp_path / "export.json"

    command = build_ncdu_export_command(
        binary="ncdu",
        target=Path("/"),
        output_path=output_path,
        one_file_system=True,
        exclude_patterns=[".cache", "node_modules"],
    )

    assert command[:4] == ["ncdu", "-o", str(output_path), "-x"]
    assert "--exclude" in command
    assert command[-1] == "/"
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python -m pytest tests/test_engine_ncdu.py -v`
Expected: FAIL with `ModuleNotFoundError` or missing symbol errors for `detect_ncdu`

- [ ] **Step 3: Write the engine adapter and verify script**

```python
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import shutil


@dataclass(frozen=True)
class EngineInfo:
    binary: str
    resolved_path: Path


def detect_ncdu(path_entries: list[str] | None = None) -> EngineInfo | None:
    resolved = shutil.which("ncdu", path=":".join(path_entries) if path_entries else None)
    if resolved is None:
        return None
    return EngineInfo(binary="ncdu", resolved_path=Path(resolved))


def build_ncdu_export_command(
    binary: str,
    target: Path,
    output_path: Path,
    one_file_system: bool,
    exclude_patterns: list[str],
) -> list[str]:
    command = [binary, "-o", str(output_path)]
    if one_file_system:
        command.append("-x")
    for pattern in exclude_patterns:
        command.extend(["--exclude", pattern])
    command.append(str(target))
    return command
```

```bash
#!/usr/bin/env bash
set -euo pipefail

if ! command -v ncdu >/dev/null 2>&1; then
  echo "ERROR: ncdu not found in PATH" >&2
  exit 127
fi

echo "ncdu_path=$(command -v ncdu)"
ncdu --version
```

- [ ] **Step 4: Run test to verify it passes**

Run: `python -m pytest tests/test_engine_ncdu.py -v`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add src/dirstat_skill/models.py src/dirstat_skill/engine_ncdu.py tests/test_engine_ncdu.py scripts/dgx/verify_ncdu.sh
git commit -m "feat: add ncdu engine detection and command builder"
```

### Task 3: Parse `ncdu` JSON Export Into Normalized Nodes

**Files:**
- Create: `Z:\Repositories\DirStat_Skill\tests\fixtures\ncdu_minimal_export.json`
- Create: `Z:\Repositories\DirStat_Skill\src\dirstat_skill\ncdu_json.py`
- Modify: `Z:\Repositories\DirStat_Skill\src\dirstat_skill\models.py`
- Create: `Z:\Repositories\DirStat_Skill\tests\test_ncdu_json.py`

- [ ] **Step 1: Write the failing parser test with a fixed fixture**

```json
[
  1,
  2,
  {
    "progname": "ncdu",
    "progver": "2.9",
    "timestamp": 1789810000
  },
  [
    {
      "name": "/sample",
      "asize": 0,
      "dsize": 4096
    },
    [
      {
        "name": "cache",
        "asize": 0,
        "dsize": 8192
      },
      {
        "name": "huge.log",
        "asize": 3221225472,
        "dsize": 3221225472
      }
    ],
    {
      "name": "notes.txt",
      "asize": 512,
      "dsize": 4096
    }
  ]
]
```

```python
from pathlib import Path

from dirstat_skill.ncdu_json import parse_ncdu_export


def test_parse_ncdu_export_flattens_directory_tree() -> None:
    fixture = Path("tests/fixtures/ncdu_minimal_export.json")

    result = parse_ncdu_export(fixture)

    assert result.root_path == "/sample"
    assert len(result.nodes) == 4
    assert result.nodes[1].path == "/sample/cache"
    assert result.nodes[2].path == "/sample/cache/huge.log"
    assert result.nodes[2].is_dir is False
    assert result.nodes[2].dsize == 3221225472
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python -m pytest tests/test_ncdu_json.py -v`
Expected: FAIL with missing parser function or incorrect node shape

- [ ] **Step 3: Implement normalized node model and parser**

```python
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class NormalizedNode:
    path: str
    name: str
    is_dir: bool
    asize: int
    dsize: int


@dataclass(frozen=True)
class ParsedExport:
    root_path: str
    nodes: list[NormalizedNode]
```

```python
from __future__ import annotations

import json
from pathlib import Path

from dirstat_skill.models import NormalizedNode, ParsedExport


def parse_ncdu_export(export_path: Path) -> ParsedExport:
    payload = json.loads(export_path.read_text(encoding="utf-8"))
    directory = payload[3]
    root_info = directory[0]
    root_path = root_info["name"]
    nodes: list[NormalizedNode] = []
    _walk_directory(directory, root_path, nodes)
    return ParsedExport(root_path=root_path, nodes=nodes)


def _walk_directory(entry: list[object], current_path: str, nodes: list[NormalizedNode]) -> None:
    info = entry[0]
    nodes.append(
        NormalizedNode(
            path=current_path,
            name=info["name"].split("/")[-1] or current_path,
            is_dir=True,
            asize=int(info.get("asize", 0)),
            dsize=int(info.get("dsize", 0)),
        )
    )
    for child in entry[1:]:
        if isinstance(child, list):
            child_info = child[0]
            child_path = f"{current_path.rstrip('/')}/{child_info['name']}"
            _walk_directory(child, child_path, nodes)
        else:
            child_path = f"{current_path.rstrip('/')}/{child['name']}"
            nodes.append(
                NormalizedNode(
                    path=child_path,
                    name=child["name"],
                    is_dir=False,
                    asize=int(child.get("asize", 0)),
                    dsize=int(child.get("dsize", 0)),
                )
            )
```

- [ ] **Step 4: Run test to verify it passes**

Run: `python -m pytest tests/test_ncdu_json.py -v`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add tests/fixtures/ncdu_minimal_export.json src/dirstat_skill/models.py src/dirstat_skill/ncdu_json.py tests/test_ncdu_json.py
git commit -m "feat: parse ncdu json exports into normalized nodes"
```

### Task 4: Implement Risk Classification And Compact Reports

**Files:**
- Create: `Z:\Repositories\DirStat_Skill\src\dirstat_skill\risk.py`
- Create: `Z:\Repositories\DirStat_Skill\src\dirstat_skill\reporting.py`
- Create: `Z:\Repositories\DirStat_Skill\tests\test_risk.py`
- Create: `Z:\Repositories\DirStat_Skill\tests\test_reporting.py`

- [ ] **Step 1: Write the failing risk and reporting tests**

```python
from dirstat_skill.models import NormalizedNode
from dirstat_skill.reporting import build_top_lists
from dirstat_skill.risk import classify_path


def test_classify_path_marks_system_prefix_as_keep_protected() -> None:
    assert classify_path("/var/lib/docker", ["/etc", "/usr", "/var/lib"], ["/home", "/var/log"]) == "keep protected"


def test_build_top_lists_filters_by_threshold_and_type() -> None:
    nodes = [
        NormalizedNode(path="/sample", name="sample", is_dir=True, asize=0, dsize=4096),
        NormalizedNode(path="/sample/cache", name="cache", is_dir=True, asize=0, dsize=8000),
        NormalizedNode(path="/sample/cache/huge.log", name="huge.log", is_dir=False, asize=0, dsize=3000),
        NormalizedNode(path="/sample/media.iso", name="media.iso", is_dir=False, asize=0, dsize=9000),
    ]

    report = build_top_lists(nodes=nodes, min_bytes=5000, top_n=5)

    assert [item.path for item in report.top_dirs] == ["/sample/cache"]
    assert [item.path for item in report.top_files] == ["/sample/media.iso"]
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `python -m pytest tests/test_risk.py tests/test_reporting.py -v`
Expected: FAIL with missing modules or missing symbols

- [ ] **Step 3: Implement the classifier and compact report builders**

```python
from __future__ import annotations


def classify_path(
    path: str,
    keep_protected_prefixes: list[str],
    review_carefully_prefixes: list[str],
) -> str:
    for prefix in keep_protected_prefixes:
        if path == prefix or path.startswith(f"{prefix.rstrip('/')}/"):
            return "keep protected"
    for prefix in review_carefully_prefixes:
        if path == prefix or path.startswith(f"{prefix.rstrip('/')}/"):
            return "review carefully"
    return "review first"
```

```python
from __future__ import annotations

from dataclasses import dataclass

from dirstat_skill.models import NormalizedNode


@dataclass(frozen=True)
class TopLists:
    top_dirs: list[NormalizedNode]
    top_files: list[NormalizedNode]


def build_top_lists(nodes: list[NormalizedNode], min_bytes: int, top_n: int) -> TopLists:
    dirs = [node for node in nodes if node.is_dir and node.dsize >= min_bytes]
    files = [node for node in nodes if not node.is_dir and node.dsize >= min_bytes]
    top_dirs = sorted(dirs, key=lambda node: node.dsize, reverse=True)[:top_n]
    top_files = sorted(files, key=lambda node: node.dsize, reverse=True)[:top_n]
    return TopLists(top_dirs=top_dirs, top_files=top_files)
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `python -m pytest tests/test_risk.py tests/test_reporting.py -v`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add src/dirstat_skill/risk.py src/dirstat_skill/reporting.py tests/test_risk.py tests/test_reporting.py
git commit -m "feat: add risk classification and compact reports"
```

### Task 5: Build The CLI And Output Writers

**Files:**
- Create: `Z:\Repositories\DirStat_Skill\src\dirstat_skill\cli.py`
- Create: `Z:\Repositories\DirStat_Skill\tests\test_cli.py`

- [ ] **Step 1: Write the failing CLI smoke test**

```python
from pathlib import Path

from dirstat_skill.cli import main


def test_cli_summarize_export_writes_summary_files(tmp_path: Path) -> None:
    export_path = Path("tests/fixtures/ncdu_minimal_export.json")
    output_dir = tmp_path / "run"

    exit_code = main(
        [
            "summarize-export",
            "--export",
            str(export_path),
            "--output-dir",
            str(output_dir),
            "--config",
            "config/defaults.json",
        ]
    )

    assert exit_code == 0
    assert (output_dir / "summary.md").exists()
    assert (output_dir / "top_dirs.csv").exists()
    assert (output_dir / "top_files.csv").exists()
    assert (output_dir / "candidates.json").exists()
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python -m pytest tests/test_cli.py -v`
Expected: FAIL with missing CLI entry point or output files

- [ ] **Step 3: Implement the CLI and output writer**

```python
from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path

from dirstat_skill.config import load_settings
from dirstat_skill.ncdu_json import parse_ncdu_export
from dirstat_skill.reporting import build_top_lists
from dirstat_skill.risk import classify_path


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="DirStat_Skill")
    subparsers = parser.add_subparsers(dest="command", required=True)

    summarize = subparsers.add_parser("summarize-export")
    summarize.add_argument("--export", required=True)
    summarize.add_argument("--output-dir", required=True)
    summarize.add_argument("--config", required=True)

    args = parser.parse_args(argv)
    if args.command == "summarize-export":
        return _summarize_export(
            export_path=Path(args.export),
            output_dir=Path(args.output_dir),
            config_path=Path(args.config),
        )
    return 2


def _summarize_export(export_path: Path, output_dir: Path, config_path: Path) -> int:
    settings = load_settings(config_path=config_path)
    parsed = parse_ncdu_export(export_path)
    top_lists = build_top_lists(parsed.nodes, min_bytes=settings.min_bytes, top_n=settings.top_n)
    output_dir.mkdir(parents=True, exist_ok=True)

    candidates = []
    for node in top_lists.top_dirs + top_lists.top_files:
        candidates.append(
            {
                "path": node.path,
                "dsize": node.dsize,
                "is_dir": node.is_dir,
                "risk": classify_path(
                    node.path,
                    settings.risk_do_not_touch_prefixes,
                    settings.risk_needs_inspection_prefixes,
                ),
            }
        )

    (output_dir / "summary.md").write_text(
        "# Audit Summary\n\n"
        f"- root: `{parsed.root_path}`\n"
        f"- top_dirs: {len(top_lists.top_dirs)}\n"
        f"- top_files: {len(top_lists.top_files)}\n",
        encoding="utf-8",
    )

    with (output_dir / "top_dirs.csv").open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=["path", "dsize"])
        writer.writeheader()
        for node in top_lists.top_dirs:
            writer.writerow({"path": node.path, "dsize": node.dsize})

    with (output_dir / "top_files.csv").open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=["path", "dsize"])
        writer.writeheader()
        for node in top_lists.top_files:
            writer.writerow({"path": node.path, "dsize": node.dsize})

    (output_dir / "candidates.json").write_text(json.dumps(candidates, indent=2), encoding="utf-8")
    return 0
```

- [ ] **Step 4: Run test to verify it passes**

Run: `python -m pytest tests/test_cli.py -v`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add src/dirstat_skill/cli.py tests/test_cli.py
git commit -m "feat: add summarize-export cli workflow"
```

### Task 6: Add DGX Runtime Wrappers And Perform Live Verification

**Files:**
- Create: `Z:\Repositories\DirStat_Skill\scripts\dgx\install_ncdu.sh`
- Create: `Z:\Repositories\DirStat_Skill\scripts\dgx\run_audit.sh`
- Modify: `Z:\Repositories\DirStat_Skill\README.md`
- Modify: `Z:\Repositories\DirStat_Skill\.agent\HANDOFF.md`

- [ ] **Step 1: Write the guarded DGX scripts**

```bash
#!/usr/bin/env bash
set -euo pipefail

if command -v ncdu >/dev/null 2>&1; then
  echo "ncdu already installed"
  exit 0
fi

if ! sudo -n true >/dev/null 2>&1; then
  echo "ERROR: sudo password required; installation must be performed with operator input" >&2
  exit 4
fi

sudo apt-get update
sudo apt-get install -y ncdu
```

```bash
#!/usr/bin/env bash
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
STAMP="$(date +%Y%m%d_%H%M_audit)"
RUN_DIR="$REPO_ROOT/outputs/$STAMP"
RAW_EXPORT="$RUN_DIR/ncdu-export.json"

mkdir -p "$RUN_DIR"
bash "$REPO_ROOT/scripts/dgx/verify_ncdu.sh"
ncdu -o "$RAW_EXPORT" -x /
python -m dirstat_skill.cli summarize-export \
  --export "$RAW_EXPORT" \
  --output-dir "$RUN_DIR" \
  --config "$REPO_ROOT/config/defaults.json"
echo "run_dir=$RUN_DIR"
```

- [ ] **Step 2: Run the automated test suite before touching the DGX**

Run: `python -m pytest tests -v`
Expected: PASS

- [ ] **Step 3: Verify whether `ncdu` already exists on DGX**

Run: `bash scripts/dgx/verify_ncdu.sh`
Expected:
- PASS path: prints `ncdu_path=...` and version
- FAIL path: exits `127` with `ERROR: ncdu not found in PATH`

- [ ] **Step 4: Attempt installation only if verify failed**

Run: `bash scripts/dgx/install_ncdu.sh`
Expected:
- PASS path: `ncdu` installs successfully
- BLOCKED path: exits `4` with `ERROR: sudo password required; installation must be performed with operator input`

- [ ] **Step 5: Perform the first live read-only run and document it**

Run: `bash scripts/dgx/run_audit.sh`
Expected:
- creates one new folder under `outputs/`
- writes `ncdu-export.json`, `summary.md`, `top_dirs.csv`, `top_files.csv`, `candidates.json`
- performs no removal operations

- [ ] **Step 6: Update docs with real commands and observed blockers**

```markdown
## First Live Run

- verify command: `bash scripts/dgx/verify_ncdu.sh`
- install command: `bash scripts/dgx/install_ncdu.sh`
- live run command: `bash scripts/dgx/run_audit.sh`
- stop condition: if `scripts/dgx/install_ncdu.sh` exits `4`, pause and request operator sudo input
```

- [ ] **Step 7: Commit**

```bash
git add scripts/dgx/install_ncdu.sh scripts/dgx/run_audit.sh README.md .agent/HANDOFF.md
git commit -m "feat: add dgx runtime wrappers and live audit flow"
```

## Self-Review

- **Spec coverage:** covered config, `ncdu` verification path, raw export parsing, compact summarization, risk classification, read-only DGX run, and sudo stop condition.
- **Placeholder scan:** no `TBD`, `TODO`, or omitted implementation sections remain in this plan.
- **Type consistency:** the plan uses `Settings`, `EngineInfo`, `NormalizedNode`, `ParsedExport`, `TopLists`, and `main()` consistently across all tasks.






