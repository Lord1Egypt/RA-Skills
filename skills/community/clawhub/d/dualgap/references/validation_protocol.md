# Validation Protocol

Use this protocol to check whether the `dualgap` skill is structurally valid and whether a workflow run produced outputs that are usable for research planning.

## Layer 1: Skill Package Validity

Run:

```powershell
python ..\skill-creator\scripts\quick_validate.py .
```

This checks `SKILL.md` frontmatter, required metadata, description length, and allowed keys.

## Layer 2: Script Integrity

Run:

```powershell
python -m py_compile scripts\run_literature_workflow.py
python -m py_compile scripts\validate_outputs.py
python -m py_compile scripts\self_validate_skill.py
```

This catches syntax and import errors before an expensive LLM batch run.

## Layer 3: Offline Self-Test

Run:

```powershell
python scripts\self_validate_skill.py
```

This wraps Layer 1 and Layer 2, validates `evals/evals.json`, creates a simulated workflow output directory, and verifies it with `scripts/validate_outputs.py`. It does not call the LLM API.

If `skill-creator/scripts/quick_validate.py` is present but cannot import `PyYAML`, the self-test falls back to a minimal built-in frontmatter validator. The JSON report marks this as `"fallback": true`; this is acceptable for portability checks, but installing `PyYAML` is still recommended before packaging a public release.

## Layer 4: Real Output Validation

After running the literature workflow, run:

```powershell
python scripts\validate_outputs.py <out-dir>
```

This checks:

- note count matches the manifest
- all per-paper notes have final passing reviews
- all five synthesis documents exist and are long enough to be substantive
- all five synthesis review JSON files exist and pass
- the audit report exists
- no obvious API key patterns appear in generated Markdown, JSON, JSONL, or text files

## Layer 5: Formal Skill-Creator Eval Loop

For a formal comparison, use the skill-creator process:

1. Keep realistic prompts in `evals/evals.json`.
2. Run a with-skill trial and a baseline trial.
3. Grade outputs against the listed expectations.
4. Aggregate with `skill-creator/scripts/aggregate_benchmark.py`.
5. Generate a review page with `skill-creator/eval-viewer/generate_review.py --static`.

Use this layer when optimizing the skill itself or comparing it against an older version.
