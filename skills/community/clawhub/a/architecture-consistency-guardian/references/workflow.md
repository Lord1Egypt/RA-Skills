# Workflow Details

Expanded guidance for each phase of the Architecture Consistency Guardian workflow.

## Phase 1 — Classification Decision Tree

```
Is the change about renaming/unifying a symbol?
  → naming

Is the change about status values, transitions, or state write-back?
  → state-machine

Is the change about where a config value is read from?
  → config-path

Is the change about which module is the sole entry point?
  → entry-point

Is the change about DB table/column names or migrations?
  → schema

Is the change about removing old code paths or fallbacks?
  → legacy-cleanup

Is the change about syncing docs/comments with code?
  → doc-alignment

Does the change span multiple repos or directories?
  → cross-module (+ one of the above as sub-category)
```

When a user reports a "bug" but the root cause is contract drift, reclassify
the task to the appropriate category above. Do not treat it as a simple bug fix.

## Phase 2 — Source of Truth Identification

### Signals of a competing source

- Two files both define `DB_PATH` or `STATUS_VALUES`
- Two modules both write to the same table
- Two functions both named `get_status()` returning different schemas
- Config read from both env var and hardcoded default in different files

### Resolution protocol

1. Check if an `ARCHITECTURE_CONTRACT.md` or equivalent exists — it is authoritative.
2. If not, identify the module that was **designed** as the owner (e.g., `runtime_config.py`
   for paths, `lifecycle_manager.py` for states).
3. If ambiguous, ask the user which source should be canonical before proceeding.

## Phase 3 — Scan Strategy

### Minimum scan scope by category

| Category | Minimum scope |
|----------|--------------|
| naming | All `.py`/`.js`/`.ts` files + all `.md` files in project |
| state-machine | All files importing the state module + DB migrations + docs |
| config-path | All files containing path literals or env var reads |
| entry-point | All files importing any of the competing entry modules |
| schema | All DB access code + migration files + ORM models |
| legacy-cleanup | All files + docs (legacy can hide anywhere) |
| doc-alignment | Code source of truth + all `.md` files |
| cross-module | All directories/repos involved |

### Scan commands

```bash
# Quick grep for old names across Python files
grep -rn "old_name" --include="*.py" /path/to/project

# Using the bundled script for structured output
python3 <skill_dir>/scripts/grep_legacy.py /path/to/project old_name_1 old_name_2

# Detect competing definitions
python3 <skill_dir>/scripts/scan_contract_drift.py /path/to/project
```

## Phase 4 — Plan Quality Checklist

Before executing, verify your plan answers:

- [ ] Is the source of truth explicitly named?
- [ ] Are ALL affected files listed (not just "and others")?
- [ ] For each file, is the specific change described?
- [ ] Are retained compatibility layers justified?
- [ ] Is the regression strategy concrete (not "run tests")?

## Phase 5 — Modification Order

Recommended sequence:

```
1. Source of truth file (define the canonical contract)
2. Direct callers / importers (update to new contract)
3. Config / env layer (unify config reads)
4. Compatibility / fallback layer (remove or mark)
5. Tests (update expectations to new contract)
6. Documentation (sync with new reality)
```

### Handling retained compatibility

When a legacy item MUST stay temporarily:

```python
# COMPAT: External module X still imports old_function().
#         Remove after X migrates (tracked in issue #123).
#         Added: 2026-04-09
def old_function():
    """Deprecated. Use new_function() instead."""
    return new_function()
```

## Phase 6 — Residue Audit Checklist

After all modifications, search for each of these:

1. **Old names**: `grep -rn "old_name" --include="*.py" --include="*.md"`
2. **Old status values**: Search for string literals of retired states
3. **Old paths**: Search for hardcoded path fragments that should use config
4. **Old imports**: Search for `from old_module import` or `import old_module`
5. **Old fallbacks**: Search for `except` or `if` blocks routing to retired logic
6. **Old docs**: Search `.md` files for retired terminology

Zero hits on retired items = clean. Any hit must be fixed or documented.

## Phase 7 — Verification Strategies by Category

| Category | Recommended verification |
|----------|------------------------|
| naming | grep old name = 0 hits; run tests |
| state-machine | grep old states = 0 hits; test state transitions |
| config-path | resolve config in real dir layout; grep old paths = 0 |
| entry-point | grep old entry imports = 0; run integration test |
| schema | compare DB columns with code references; run migrations |
| legacy-cleanup | grep old names = 0; run full test suite |
| doc-alignment | diff doc descriptions against code behavior |
| cross-module | run tests in each repo; cross-grep for old names |

## Edge Cases

### User says "just fix this one file"

Even if the user scopes narrowly, do a **quick 30-second scan** for global impact.
If you find cross-file references, inform the user:
> "This name also appears in X, Y, Z. Fixing only the current file will leave
> inconsistencies. Recommend expanding scope."

Let the user decide, but make the risk visible.

### No test suite exists

When there are no tests:
1. Use grep-based residue audit as primary verification
2. Run the modified code path if possible (e.g., `python -c "from module import func"`)
3. Note the lack of test coverage as a follow-up risk in the report

### Change spans repos with different owners

1. Complete changes in the repo you control
2. Document the required changes in other repos
3. List them as "pending external changes" in the report
4. Suggest creating issues/PRs for the external repos
