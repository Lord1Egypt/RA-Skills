---
name: skill-forge
category: tool
description: "从需求描述或已有 SKILL.md 生成完整的可评估 Skill。核心能力: 自动生成 task_suite.yaml 测试任务集。当需要为新 Skill 创建测试、为已有 Skill 补充测试、或从零创建可验证的 Skill 时使用。"
license: MIT
triggers:
  - forge skill
  - generate skill
  - create task suite
  - 生成技能
  - 创建测试任务
  - 补充task suite
---

# Skill Forge

Generate Skills from requirements AND generate `task_suite.yaml` for evaluation.

The primary value of this skill is **task_suite generation** -- turning a SKILL.md into a structured test harness that `improvement-evaluator` can run. Secondary value is generating SKILL.md from a structured spec.

## When to Use

1. **Add tests to an existing Skill** -- You have a SKILL.md but no task_suite.yaml. Use `--from-skill` to analyze the skill and generate a test suite automatically.
2. **Create a new Skill from scratch** -- You have a YAML spec describing what the skill should do. Use `--from-spec` to generate both SKILL.md and task_suite.yaml.
3. **Full lifecycle** -- Generate a skill, test it, evaluate it, and optionally improve it in one pass.

## When NOT to Use

- You just want to **evaluate** an existing skill with an existing task_suite → use `improvement-evaluator`
- You just want to **improve** a skill that already has tests → use `improvement-orchestrator`
- You want to **manually write** a SKILL.md → use `skill-creator`

## Modes

### Mode A: `--from-skill` (Generate task suite for existing SKILL.md)

```bash
python3 scripts/forge.py --from-skill /path/to/skill-dir --output /path/to/output
```

Reads the SKILL.md, extracts scenarios from:
- Frontmatter (description, triggers)
- "When to Use" bullets → positive test tasks
- `<example>` tags → expected-output tests
- `<anti-example>` tags → negative tests (should avoid bad patterns)
- Output format/CLI sections → format compliance tests

Produces `task_suite.yaml` in the output directory.

### Mode B: `--from-spec` (Generate skill + task suite from spec)

```bash
python3 scripts/forge.py --from-spec spec.yaml --output /path/to/output
```

Reads a `skill_spec.yaml` (see `references/spec-format.md`) and generates:
1. A complete SKILL.md with frontmatter, sections, examples
2. A task_suite.yaml derived from the generated SKILL.md

### Common Flags

| Flag | Effect |
|------|--------|
| `--mock` | Use mock LLM (for testing without API calls) |
| `--evaluate` | Run `improvement-evaluator` after generation (requires it installed) |
| `--auto-improve` | Run `improvement-orchestrator` if score below SOLID (requires it installed) |

## Output Artifacts

| Request | Deliverable |
|---------|------------|
| `--from-skill` | `task_suite.yaml` with 5-10 test tasks |
| `--from-spec` | `SKILL.md` + `task_suite.yaml` |
| `--evaluate` | Evaluation report (pass/fail per task) |

## Task Generation Strategy

The generator extracts test scenarios from 5 sources in the SKILL.md:

1. **Frontmatter description** → 1 core-capability test
2. **"When to Use" section** → up to 3 positive use-case tests
3. **`<example>` tags** → up to 2 keyword-match tests
4. **`<anti-example>` tags** → up to 2 anti-pattern avoidance tests
5. **Output format section** → 1 format compliance test

Tasks are deduplicated and capped at 10 per suite.

### Judge Selection

- Scenario with specific keywords/outputs → `ContainsJudge`
- Scenario requiring quality/style assessment → `LLMRubricJudge`
- Scenario with structured output → `PytestJudge` (if test script can be generated)

### Harness Pattern Tasks (for scripted skills)

When the target skill has a `scripts/` directory, forge auto-generates additional test tasks checking execution-harness pattern adoption:

- **Timeout handling**: Does the skill handle `subprocess.TimeoutExpired`?
- **Atomic writes**: Does it use `write_json`/`write_text` from `lib/common` (atomic write-then-rename)?
- **Backup/rollback**: Does it create backups before file modifications?
- **Error escalation**: Does it have graduated error handling (not just crash-on-first-failure)?
- **State persistence**: Does it write recoverable state for crash recovery?

These tasks use `ContainsJudge` to grep the skill's Python source code. They only apply to orchestration/tool-type skills — pure-text knowledge skills skip this category.

### Null-Skill Calibration

Tasks that a "null skill" (empty context, no SKILL.md loaded) would trivially pass are filtered out. This prevents inflated scores from tasks that test general LLM capability rather than the skill's specific value.

## Related Skills

| Skill | Relationship |
|-------|-------------|
| `improvement-evaluator` | Runs the generated task_suite.yaml |
| `improvement-orchestrator` | Drives generate → evaluate → improve loop |
| `improvement-generator` | Generates improvement candidates for skills |
| `skill-creator` | Manual SKILL.md authoring guide |
