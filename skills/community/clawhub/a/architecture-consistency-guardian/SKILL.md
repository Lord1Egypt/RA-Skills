---
name: architecture-consistency-guardian
description: >
  Enforce system-wide consistency before code changes. Activate for any task involving:
  refactoring across files, unifying variable/field/parameter names, consolidating state machines,
  cleaning legacy paths or fallbacks, aligning configuration sources, unifying database schema,
  consolidating service entry points, aligning documentation with code, or preventing local-only
  fixes that ignore global architecture contracts.

  Trigger signals: "统一一下", "全局改", "别只修当前文件", "检查所有引用", "清理 legacy",
  "状态机不统一", "配置路径不一致", "多个模块都要改", "架构收口", "重构", "修复兼容层",
  "把新旧逻辑统一", "unify", "consolidate", "clean up legacy", "align across modules",
  "single source of truth", "remove fallback", "schema drift".

  Also activate when a reported bug may stem from contract drift (e.g., mismatched field names,
  stale fallback paths, dual write targets, or status values not in the canonical set).

  NOT for: pure greenfield feature development with no cross-file impact, cosmetic lint/format
  changes, or single-file typo fixes with zero external references.
---

# Architecture Consistency Guardian

## Purpose

Force a **global-first** posture for every code change that touches shared contracts:
names, states, paths, configs, schemas, entry points, fallbacks, or documentation.

The default agent behavior is to patch the immediate error site. This skill overrides
that instinct: **scan globally, identify the single source of truth, modify as a group,
audit for residue, then verify.**

## Mandatory Workflow (8 phases)

Every task under this skill MUST follow these phases in order.
Skip a phase only if you can explicitly justify why it does not apply.

### Phase 1 — Classify the Task

Determine which consistency category applies:

| Category | Examples |
|----------|----------|
| naming | Variable, field, parameter, event name unification |
| state-machine | Status values, transition rules, write-back entry |
| config-path | DB path, env var, runtime config, deploy assumption |
| entry-point | Consolidating orchestrator / service / manager as sole entry |
| schema | Table name, column name, migration, compatibility layer |
| legacy-cleanup | Removing old fallback, old table writes, old function names |
| doc-alignment | Syncing SKILL.md, README, comments, contract docs with code |
| cross-module | Multi-repo or multi-directory coordinated change |

If multiple categories apply, lead with the one closest to the source of truth.

### Phase 2 — Identify the Single Source of Truth

Answer explicitly before writing any code:

1. What is the **canonical file/module** for this contract?
2. Are there **competing sources**? List them.
3. Which one survives, which ones get retired?

If no architecture contract document exists, produce a **temporary contract summary**
(inline in your plan) covering: canonical state field, canonical write entry, canonical
config source, and legacy items to retire. Read `references/contract_template.md` for
the template when creating a persistent contract file.

### Phase 3 — Global Reference Scan

Search the **entire relevant scope** (not just the current file) for:

- Old and new variable/field names
- Old and new status values
- Hardcoded paths or env vars that should come from config
- Old table names or column names
- Old function/method names
- Fallback branches that route to retired logic
- Documentation still describing old flows

Use `scripts/grep_legacy.py` when available:
```bash
python3 <skill_dir>/scripts/grep_legacy.py <directory> <pattern1> <pattern2> ...
```

Use `scripts/scan_contract_drift.py` for multi-source detection:
```bash
python3 <skill_dir>/scripts/scan_contract_drift.py <directory> [--pattern-file <file>] [--mode default|lite|strict]
```

Mode guidance:
- `default`: best general-purpose mode; ignores reference/template/test-only mentions as evidence
- `lite`: same filtering as `default`, but down-ranks lower-risk categories for quick triage
- `strict`: count every matching file, including references and tests, for forensic audits

### Lite Mode

For small consistency fixes touching only 2-3 files with one clear source of truth,
you may run a lite variant of the workflow:

1. Classify the task
2. Identify the source of truth
3. Run a scoped global reference scan
4. Output a short modification plan
5. Edit all affected files in one pass
6. Run a residue search for the retired names/paths
7. Verify with at least one focused check

Use full 8-phase mode for state machines, schema changes, config paths, entry-point
consolidation, or any task where multiple competing truths may exist.

### Phase 4 — Produce a Modification Plan

Before touching code, output a concise plan:

1. **Source of truth** — the canonical file
2. **Affected files** — full list
3. **Changes per file** — what gets renamed/removed/updated
4. **Compatibility layers to remove or retain** (with justification if retained)
5. **Regression strategy** — how you will verify

Do NOT proceed to edits without this plan.

### Phase 5 — Execute Grouped Modifications

Recommended order: **source of truth → callers → config layer → compatibility layer → tests → docs**.

Rules:
- Modify all references in a single logical pass; do not leave half-renamed states.
- If a legacy item must be temporarily retained, mark it with a comment:
  `# COMPAT: <reason> — remove by <date or condition>`
- Never silently keep old logic alive.

### Phase 6 — Residue Audit

After all edits, actively search for:

1. Old variable/field names still present
2. Old status values still present
3. Old paths or env vars still present
4. Old fallback branches still present
5. Docs, comments, or SKILL files still referencing old flow

Use `scripts/grep_legacy.py` again with the retired names.
**If any residue is found, either fix it or explicitly document why it remains.**

### Phase 7 — Regression Verification

Execute at least one of:
- Run existing test suite
- Run a minimal script verifying the changed contract
- Search for old names (zero hits expected)
- Validate schema against code references
- Confirm config resolution in the real directory layout

### Phase 8 — Structured Report

Every task MUST end with a report containing these sections:

| Section | Required | Content |
|---------|----------|---------|
| Classification | ✅ | Which consistency category |
| Source of truth | ✅ | The canonical location |
| Scope | ✅ | Files/modules affected |
| Changes made | ✅ | Concrete list of modifications |
| Residual compat | ✅ | What old logic remains and why |
| Verification | ✅ | What checks were performed |
| Follow-up risks | Recommended | Next steps or remaining debt |

Read `references/output_template.md` for the full report template.

## Hard Rules

These are non-negotiable constraints:

1. **Never modify only the error site** when the root cause is a contract mismatch.
2. **Never rename a symbol in one file** without searching all files for the old name.
3. **Never delete a legacy path** without confirming no external module depends on it.
4. **Never keep a fallback silently** — if it stays, it gets a COMPAT comment and a reason.
5. **Never report "fixed"** without stating what residue remains.
6. **Never skip doc/comment updates** when code behavior changes.
7. **Always expand scope** when the change touches: config vars, env vars, DB paths,
   table/column names, status fields, status values, event names, service entry points,
   fallback logic, or documented main paths.

## When to Suggest an Architecture Contract File

If you observe any of these recurring in a project, recommend creating an
`ARCHITECTURE_CONTRACT.md` (template in `references/contract_template.md`):

- Multiple status fields coexisting for the same entity
- Multiple config entry points for the same value
- Multiple write paths for the same data store
- Docs and code chronically out of sync
- Repeated legacy/new path confusion across tasks

## References

- `references/workflow.md` — Detailed workflow with decision branches and edge cases
- `references/output_template.md` — Structured report template
- `references/risk_patterns.md` — Common consistency risk patterns with examples
- `references/contract_template.md` — Architecture contract template for projects lacking one

## Scripts

- `scripts/grep_legacy.py` — Scan directories for legacy name/path/status residue
- `scripts/scan_contract_drift.py` — Detect multiple competing sources of truth; supports `--mode default|lite|strict`
- `scripts/summarize_impacts.py` — Aggregate scan results into an impact summary
