# DirStat_Skill Recursive Review Report Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Replace flat `top_n`-style reporting with a recursive 80/20 dossier that emits full-path review candidates, reasons, and dependency-check evidence under `outputs/`.

**Architecture:** Keep scan engines unchanged and refactor the reporting stage into a deterministic selection pipeline: normalized nodes -> recursive dominant-branch walk -> candidate dossier rows -> Markdown/CSV/JSON outputs. Dependency checks stay cheap and local by combining heuristic signatures with nearby reference scans around each candidate.

**Tech Stack:** Python 3.12, stdlib filesystem tools, existing `dirstat_skill` models/CLI/tests, `pytest`

---

## File Structure

- Modify: `src/dirstat_skill/models.py`
  - add typed structures for dossier candidates and report metadata
- Modify: `src/dirstat_skill/reporting.py`
  - implement recursive dominant-branch selection, candidate construction, and output rendering helpers
- Modify: `src/dirstat_skill/cli.py`
  - replace the old flat summary writer with the new dossier bundle writer
- Modify: `src/dirstat_skill/config.py`
  - load new report-tuning settings
- Modify: `config/defaults.json`
  - add deterministic defaults for recursive reporting and nearby-ref checks
- Modify: `README.md`
  - document the new output contract and semantics
- Modify: `skills/DirStat_Skill/SKILL.md`
  - describe the dossier outputs and 80/20 walk
- Test: `tests/test_reporting.py`
  - cover recursive selection and dossier rendering
- Test: `tests/test_cli.py`
  - verify output bundle creation

### Task 1: Add Candidate Models And Config

**Files:**
- Modify: `src/dirstat_skill/models.py`
- Modify: `src/dirstat_skill/config.py`
- Modify: `config/defaults.json`
- Test: `tests/test_config.py`

- [ ] **Step 1: Write the failing config test**

```python
def test_load_settings_reads_recursive_reporting_defaults() -> None:
    settings = load_settings(Path("config/defaults.json"))

    assert settings.dominant_percent == 0.8
    assert settings.max_nearby_reference_files > 0
    assert ".json" in settings.nearby_reference_extensions
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python -m pytest tests/test_config.py::test_load_settings_reads_recursive_reporting_defaults -v`
Expected: FAIL because the new settings fields do not exist yet.

- [ ] **Step 3: Add typed config and dossier models**

```python
@dataclass(frozen=True)
class ReviewCandidate:
    path: str
    dsize: int
    is_dir: bool
    bucket: str
    review_reason: str
    dependency_check_summary: str
    dependency_check_confidence: str
    selection_source: str
```

```python
@dataclass(frozen=True)
class Settings:
    ...
    dominant_percent: float
    max_nearby_reference_files: int
    nearby_reference_extensions: list[str]
```

- [ ] **Step 4: Run the focused config test**

Run: `python -m pytest tests/test_config.py::test_load_settings_reads_recursive_reporting_defaults -v`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add src/dirstat_skill/models.py src/dirstat_skill/config.py config/defaults.json tests/test_config.py
git commit -m "feat: add recursive reporting config"
```

### Task 2: Implement Recursive 80/20 Selection

**Files:**
- Modify: `src/dirstat_skill/reporting.py`
- Test: `tests/test_reporting.py`

- [ ] **Step 1: Write the failing selection test**

```python
def test_select_dominant_nodes_walks_recursively_until_concrete_candidates() -> None:
    nodes = [
        NormalizedNode(path="/root", name="root", is_dir=True, asize=0, dsize=1000),
        NormalizedNode(path="/root/a", name="a", is_dir=True, asize=0, dsize=850),
        NormalizedNode(path="/root/b", name="b", is_dir=True, asize=0, dsize=150),
        NormalizedNode(path="/root/a/f1.bin", name="f1.bin", is_dir=False, asize=0, dsize=500),
        NormalizedNode(path="/root/a/f2.bin", name="f2.bin", is_dir=False, asize=0, dsize=350),
    ]

    selected = select_dominant_candidates(nodes, root_path="/root", dominant_percent=0.8, min_candidate_bytes=100)

    assert [item.path for item in selected] == ["/root/a/f1.bin", "/root/a/f2.bin"]
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python -m pytest tests/test_reporting.py::test_select_dominant_nodes_walks_recursively_until_concrete_candidates -v`
Expected: FAIL because `select_dominant_candidates` does not exist.

- [ ] **Step 3: Implement the recursive selector**

```python
def select_dominant_candidates(
    nodes: list[NormalizedNode],
    root_path: str,
    dominant_percent: float,
    min_candidate_bytes: int,
) -> list[NormalizedNode]:
    ...
```

Implementation requirements:

- build parent -> child indexes once
- sort children by `dsize` descending
- keep children until cumulative share reaches `dominant_percent`
- recurse into dominant directories
- stop on files, protected paths, flat distributions, or size threshold

- [ ] **Step 4: Add two more failing tests before widening the implementation**

```python
def test_select_dominant_candidates_keeps_flat_directory_when_no_clear_winner() -> None:
    ...

def test_select_dominant_candidates_keeps_many_medium_files_that_dominate_together() -> None:
    ...
```

- [ ] **Step 5: Run the reporting tests**

Run: `python -m pytest tests/test_reporting.py -v`
Expected: PASS

- [ ] **Step 6: Commit**

```bash
git add src/dirstat_skill/reporting.py tests/test_reporting.py
git commit -m "feat: add recursive 80-20 candidate selection"
```

### Task 3: Add Dependency Check And Dossier Rendering

**Files:**
- Modify: `src/dirstat_skill/reporting.py`
- Test: `tests/test_reporting.py`

- [ ] **Step 1: Write the failing dossier test**

```python
def test_build_review_candidates_adds_reason_and_dependency_summary() -> None:
    nodes = [
        NormalizedNode(path="/home/user/.cache/blob.bin", name="blob.bin", is_dir=False, asize=0, dsize=2000),
    ]

    candidates = build_review_candidates(
        selected_nodes=nodes,
        all_nodes=nodes,
        protected_prefixes=["/etc", "/usr", "/var/lib"],
        inspection_prefixes=["/home"],
        nearby_reference_extensions=[".json", ".yaml"],
        max_nearby_reference_files=5,
    )

    assert candidates[0].review_reason
    assert "cache" in candidates[0].dependency_check_summary.lower()
    assert candidates[0].bucket == "review first"
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python -m pytest tests/test_reporting.py::test_build_review_candidates_adds_reason_and_dependency_summary -v`
Expected: FAIL because dossier-building helpers do not exist.

- [ ] **Step 3: Implement dependency-check helpers and output renderers**

```python
def build_review_candidates(...) -> list[ReviewCandidate]:
    ...

def render_review_report(...) -> str:
    ...

def write_review_candidates_csv(...) -> None:
    ...
```

Implementation requirements:

- heuristics first for cache/temp/trash/partial/system paths
- nearby-ref scan second for ambiguous user-owned assets
- confidence levels limited to `high`, `medium`, `low`
- report sections grouped by `bucket`

- [ ] **Step 4: Add focused tests for protected paths and ambiguous model assets**

```python
def test_build_review_candidates_marks_system_storage_as_keep_protected() -> None:
    ...

def test_build_review_candidates_marks_user_model_without_nearby_refs_as_review_carefully() -> None:
    ...
```

- [ ] **Step 5: Run the reporting tests**

Run: `python -m pytest tests/test_reporting.py -v`
Expected: PASS

- [ ] **Step 6: Commit**

```bash
git add src/dirstat_skill/reporting.py tests/test_reporting.py
git commit -m "feat: add review dossier rendering"
```

### Task 4: Wire The New Outputs Through The CLI

**Files:**
- Modify: `src/dirstat_skill/cli.py`
- Test: `tests/test_cli.py`

- [ ] **Step 1: Write the failing CLI output test**

```python
def test_cli_audit_writes_recursive_review_bundle(tmp_path: Path) -> None:
    ...
    assert (output_dir / "review_report.md").exists()
    assert (output_dir / "review_candidates.csv").exists()
    assert (output_dir / "candidates.json").exists()
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python -m pytest tests/test_cli.py::test_cli_audit_writes_recursive_review_bundle -v`
Expected: FAIL because the CLI does not write the new dossier files.

- [ ] **Step 3: Replace the old flat writer call with the dossier pipeline**

```python
selected_nodes = select_dominant_candidates(...)
candidates = build_review_candidates(...)
write_review_bundle(...)
```

- [ ] **Step 4: Run CLI tests**

Run: `python -m pytest tests/test_cli.py -v`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add src/dirstat_skill/cli.py tests/test_cli.py
git commit -m "feat: emit recursive review dossier"
```

### Task 5: Update Public Docs

**Files:**
- Modify: `README.md`
- Modify: `skills/DirStat_Skill/SKILL.md`

- [ ] **Step 1: Update README output contract**

```md
- `review_candidates.csv`
- `review_report.md`
- recursive 80/20 walk over dominant branches
```

- [ ] **Step 2: Update skill workflow**

```md
Read `review_report.md` first, then `review_candidates.csv`, then `candidates.json` for machine-readable detail.
```

- [ ] **Step 3: Run the full test suite**

Run: `python -m pytest tests -v`
Expected: PASS

- [ ] **Step 4: Commit**

```bash
git add README.md skills/DirStat_Skill/SKILL.md
git commit -m "docs: describe recursive review dossier"
```

## Self-Review

- Spec coverage:
  - recursive 80/20 walk: Task 2
  - dependency checks and reasons: Task 3
  - expanded output contract: Tasks 3 and 4
  - docs/config coherence: Tasks 1 and 5
- Placeholder scan:
  - no `TODO`, `TBD`, or vague “handle edge cases” steps remain
- Type consistency:
  - `ReviewCandidate`, `select_dominant_candidates`, and dossier filenames are named consistently across tasks

## Execution Handoff

Plan complete and saved to `docs/superpowers/plans/2026-09-19-dirstat-skill-recursive-report.md`.

Two execution options:

1. Subagent-Driven (recommended) - I dispatch a fresh subagent per task, review between tasks, fast iteration
2. Inline Execution - Execute tasks in this session using executing-plans, batch execution with checkpoints

