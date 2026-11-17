# DirStat_Skill Analysis Dossier Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Refactor `DirStat_Skill` so the public dossier reports explicit analysis types, surfaces probable duplicates and protected huge hotspots, and allows runtime override of the dominant-space threshold.

**Architecture:** Keep the existing scan engines and runtime guardrails intact. Refactor the reporting layer into a richer finding model, add lightweight duplicate and hotspot analyses, and thread a CLI override for `dominant_percent` from config/CLI into the output artifacts and public documentation.

**Tech Stack:** Python 3.12, argparse, dataclasses, existing `dirstat_skill` modules, `pytest`, Markdown docs

---

## File Structure

- Modify: `Z:\Repositories\DirStat_Skill\src\dirstat_skill\models.py`
  - replace the narrow review-candidate shape with a richer finding model
- Modify: `Z:\Repositories\DirStat_Skill\src\dirstat_skill\reporting.py`
  - add analysis-kind findings, duplicate grouping, protected hotspot surfacing, and new report rendering
- Modify: `Z:\Repositories\DirStat_Skill\src\dirstat_skill\config.py`
  - allow runtime override of `dominant_percent`
- Modify: `Z:\Repositories\DirStat_Skill\src\dirstat_skill\cli.py`
  - add `--dominant-percent` and pass the actual runtime value through reporting
- Modify: `Z:\Repositories\DirStat_Skill\config\defaults.json`
  - keep default `dominant_percent` and add any minimal thresholds needed for new analyses
- Modify: `Z:\Repositories\DirStat_Skill\README.md`
- Modify: `Z:\Repositories\DirStat_Skill\AGENTS.md`
- Modify: `Z:\Repositories\DirStat_Skill\skills\DirStat_Skill\SKILL.md`
- Test: `Z:\Repositories\DirStat_Skill\tests\test_reporting.py`
- Test: `Z:\Repositories\DirStat_Skill\tests\test_cli.py`
- Test: `Z:\Repositories\DirStat_Skill\tests\test_config.py`

### Task 1: Add Runtime Override For Dominant Percent

**Files:**
- Modify: `Z:\Repositories\DirStat_Skill\src\dirstat_skill\config.py`
- Modify: `Z:\Repositories\DirStat_Skill\src\dirstat_skill\cli.py`
- Test: `Z:\Repositories\DirStat_Skill\tests\test_config.py`
- Test: `Z:\Repositories\DirStat_Skill\tests\test_cli.py`

- [ ] **Step 1: Write the failing config and CLI tests**

```python
def test_load_settings_reads_dominant_percent_override() -> None:
    settings = load_settings(
        Path("config/defaults.json"),
        env_overrides={"DOMINANT_PERCENT": "0.67"},
    )
    assert settings.dominant_percent == 0.67


def test_cli_summarize_export_accepts_dominant_percent_override(tmp_path: Path) -> None:
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
            "--dominant-percent",
            "0.67",
        ]
    )
    assert exit_code == 0
    payload = json.loads((output_dir / "candidates.json").read_text(encoding="utf-8"))
    assert all(item["configured_dominant_percent"] == 0.67 for item in payload)
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `python -m pytest tests/test_config.py tests/test_cli.py -k "dominant_percent_override or dominant_percent" -v`
Expected: FAIL because the override is not wired through runtime yet.

- [ ] **Step 3: Implement the runtime override**

```python
dominant_override = overrides.get("DOMINANT_PERCENT")
dominant_percent = float(dominant_override) if dominant_override is not None else float(payload.get("dominant_percent", 0.8))
```

```python
summarize.add_argument("--dominant-percent", type=float, default=None)
audit.add_argument("--dominant-percent", type=float, default=None)
```

- [ ] **Step 4: Re-run the focused tests**

Run: `python -m pytest tests/test_config.py tests/test_cli.py -k "dominant_percent_override or dominant_percent" -v`
Expected: PASS

### Task 2: Replace ReviewCandidate With A Richer Finding Model

**Files:**
- Modify: `Z:\Repositories\DirStat_Skill\src\dirstat_skill\models.py`
- Modify: `Z:\Repositories\DirStat_Skill\src\dirstat_skill\reporting.py`
- Test: `Z:\Repositories\DirStat_Skill\tests\test_reporting.py`

- [ ] **Step 1: Write the failing reporting test**

```python
def test_build_findings_emits_analysis_kind_and_evidence(tmp_path: Path) -> None:
    cache_dir = tmp_path / ".cache"
    cache_dir.mkdir()
    blob_path = cache_dir / "blob.bin"
    blob_path.write_bytes(b"x")
    nodes = [NormalizedNode(path=str(blob_path), name="blob.bin", is_dir=False, asize=0, dsize=2000)]
    findings = build_analysis_findings(
        selected_nodes=nodes,
        all_nodes=nodes,
        protected_prefixes=["/etc", "/usr", "/var/lib"],
        inspection_prefixes=[str(tmp_path)],
        nearby_reference_extensions=[".json"],
        max_nearby_reference_files=5,
        dominant_percent=0.8,
    )
    assert findings[0].analysis_kind == "signature heuristics"
    assert findings[0].evidence
    assert findings[0].configured_dominant_percent == 0.8
```

- [ ] **Step 2: Run the focused reporting test**

Run: `python -m pytest tests/test_reporting.py -k "analysis_kind_and_evidence" -v`
Expected: FAIL because the richer finding model does not exist yet.

- [ ] **Step 3: Implement the new finding model and builder**

```python
@dataclass(frozen=True)
class AnalysisFinding:
    path: str
    dsize: int
    is_dir: bool
    analysis_kind: str
    attention_level: str
    review_reason: str
    evidence: str
    dependency_check_confidence: str
    selection_source: str
    group_key: str
    configured_dominant_percent: float
```

- [ ] **Step 4: Re-run the focused reporting test**

Run: `python -m pytest tests/test_reporting.py -k "analysis_kind_and_evidence" -v`
Expected: PASS

### Task 3: Add Probable Duplicate And Protected Hotspot Analyses

**Files:**
- Modify: `Z:\Repositories\DirStat_Skill\src\dirstat_skill\reporting.py`
- Test: `Z:\Repositories\DirStat_Skill\tests\test_reporting.py`

- [ ] **Step 1: Write the failing duplicate and hotspot tests**

```python
def test_build_findings_surfaces_probable_duplicates(tmp_path: Path) -> None:
    a_dir = tmp_path / "a"
    b_dir = tmp_path / "b"
    a_dir.mkdir()
    b_dir.mkdir()
    first = a_dir / "model.safetensors"
    second = b_dir / "model.safetensors"
    first.write_bytes(b"x")
    second.write_bytes(b"y")
    nodes = [
        NormalizedNode(path=str(first), name="model.safetensors", is_dir=False, asize=0, dsize=2000),
        NormalizedNode(path=str(second), name="model.safetensors", is_dir=False, asize=0, dsize=2000),
    ]
    findings = build_analysis_findings(...)
    assert any(item.analysis_kind == "probable duplicates" for item in findings)


def test_build_findings_surfaces_protected_huge_hotspot() -> None:
    nodes = [
        NormalizedNode(path="/var/lib/docker-loop.xfs", name="docker-loop.xfs", is_dir=False, asize=0, dsize=2000),
    ]
    findings = build_analysis_findings(...)
    assert any(item.analysis_kind == "protected huge hotspots" for item in findings)
```

- [ ] **Step 2: Run the focused tests**

Run: `python -m pytest tests/test_reporting.py -k "probable_duplicates or protected_huge_hotspot" -v`
Expected: FAIL because these analyses are not yet emitted.

- [ ] **Step 3: Implement duplicate and hotspot emitters**

```python
def _build_probable_duplicate_findings(nodes: list[NormalizedNode], dominant_percent: float) -> list[AnalysisFinding]:
    ...


def _build_protected_hotspot_findings(selected_nodes: list[NormalizedNode], protected_prefixes: list[str], dominant_percent: float) -> list[AnalysisFinding]:
    ...
```

- [ ] **Step 4: Re-run the focused tests**

Run: `python -m pytest tests/test_reporting.py -k "probable_duplicates or protected_huge_hotspot" -v`
Expected: PASS

### Task 4: Render The Analysis Dossier And Update Output Files

**Files:**
- Modify: `Z:\Repositories\DirStat_Skill\src\dirstat_skill\reporting.py`
- Modify: `Z:\Repositories\DirStat_Skill\src\dirstat_skill\cli.py`
- Test: `Z:\Repositories\DirStat_Skill\tests\test_reporting.py`
- Test: `Z:\Repositories\DirStat_Skill\tests\test_cli.py`

- [ ] **Step 1: Write the failing report-render test**

```python
def test_render_review_report_shows_analysis_sections(tmp_path: Path) -> None:
    findings = [
        AnalysisFinding(
            path="/var/lib/docker-loop.xfs",
            dsize=2000,
            is_dir=False,
            analysis_kind="protected huge hotspots",
            attention_level="keep protected",
            review_reason="protected runtime area dominates space",
            evidence="protected prefix matched with large size",
            dependency_check_confidence="high",
            selection_source="dominant_leaf",
            group_key="hotspot:/var/lib",
            configured_dominant_percent=0.8,
        )
    ]
    report = render_review_report("/", findings)
    assert "## Protected Huge Hotspots" in report
    assert "configured_dominant_percent" in report
```

- [ ] **Step 2: Run the focused tests**

Run: `python -m pytest tests/test_reporting.py tests/test_cli.py -k "analysis_sections or summarize_export_writes_summary_files" -v`
Expected: FAIL because the dossier still renders old category sections only.

- [ ] **Step 3: Implement the new render and wire it through the CLI**

```python
(output_dir / "candidates.json").write_text(
    json.dumps([finding.__dict__ for finding in findings], indent=2),
    encoding="utf-8",
)
write_review_candidates_csv(output_dir / "review_candidates.csv", findings)
(output_dir / "review_report.md").write_text(
    render_review_report(parsed.root_path, findings),
    encoding="utf-8",
)
```

- [ ] **Step 4: Re-run the focused tests**

Run: `python -m pytest tests/test_reporting.py tests/test_cli.py -k "analysis_sections or summarize_export_writes_summary_files" -v`
Expected: PASS

### Task 5: Update README, AGENTS, And SKILL For Interpretation

**Files:**
- Modify: `Z:\Repositories\DirStat_Skill\README.md`
- Modify: `Z:\Repositories\DirStat_Skill\AGENTS.md`
- Modify: `Z:\Repositories\DirStat_Skill\skills\DirStat_Skill\SKILL.md`

- [ ] **Step 1: Update README to explain the six analyses and runtime override**

```md
## How To Read Results

Read in this order:

1. `review_report.md`
2. `review_candidates.csv`
3. `summary.md`
4. `candidates.json`

## Analysis Types

- `dominant space`
- `path safety`
- `nearby references`
- `signature heuristics`
- `probable duplicates`
- `protected huge hotspots`
```

- [ ] **Step 2: Update AGENTS and SKILL to match the same vocabulary**

```md
- the dossier is analysis-driven
- read `review_report.md` first
- treat `probable duplicates` as a suspicion, not proof
- treat `protected huge hotspots` as visibility-only, not an action cue
```

- [ ] **Step 3: Run the full suite**

Run: `python -m pytest tests -q`
Expected: PASS

### Task 6: Verify, Push, And Check OpenClaw Alignment

**Files:**
- Modify if needed: `Z:\Repositories\DirStat_Skill\.agent\HANDOFF.md`
- Verify script path: `Z:\Repositories\trash\check_openclaw_dirstat_link.sh`

- [ ] **Step 1: Run final verification**

Run: `python -m pytest tests -q`
Expected: PASS

- [ ] **Step 2: Verify Git state and push**

Run: `git status --short`
Expected: only intended changes

Run: `git push origin main`
Expected: push succeeds

- [ ] **Step 3: Verify OpenClaw symlink alignment**

Run: `ssh dgx "bash /home/jagones/Repositories/trash/check_openclaw_dirstat_link.sh"`
Expected:
- `ACTIVE_IS_SYMLINK=yes`
- `WORKSPACE_IS_SYMLINK=yes`
- final resolved path is `/home/jagones/Repositories/DirStat_Skill/skills/DirStat_Skill`
