---
name: skill-forge
category: tool
description: >
  当需要为已有 Skill 自动生成 task_suite.yaml 测试任务集、从 skill_spec.yaml
  生成完整 SKILL.md + task_suite、或一键走完「生成 → 评估 → 改进」全链路时使用。
  读取 SKILL.md 中的 frontmatter/When to Use/example/anti-example/Output 五类来源，
  自动推导 5-10 个 test task 并选择 ContainsJudge / LLMRubricJudge / PytestJudge。
  不用于手动编写 SKILL.md（用 skill-creator）、单独评估已有 task_suite（用 improvement-evaluator）、
  或驱动改进循环（用 improvement-orchestrator）。
license: MIT
triggers:
  - forge skill
  - generate skill
  - create task suite
  - generate task suite
  - forge test
  - from spec generate
  - null-skill calibration
  - 生成技能
  - 创建测试任务
  - 补充task suite
  - 为 skill 生成测试
  - 从 spec 创建 skill
---

# Skill Forge

Generate Skills from requirements AND generate `task_suite.yaml` for evaluation.

The primary value of this skill is **task_suite generation** -- turning a SKILL.md into a structured test harness that `improvement-evaluator` can run. Secondary value is generating SKILL.md from a structured `skill_spec.yaml`.

**Key differentiator**: Skill Forge does not merely scaffold a skeleton; it performs static analysis of the SKILL.md to extract testable claims (from five distinct sources) and assigns the appropriate judge type per task, producing a suite that is immediately runnable by `improvement-evaluator`.

## When to Use

1. **Add tests to an existing Skill** -- You have a SKILL.md but no `task_suite.yaml`.
   Run `--from-skill` to analyze the SKILL.md and generate a test suite automatically.
   The generator extracts scenarios from five sections of the document and assigns
   the right judge per task.
2. **Create a new Skill from scratch** -- You have a `skill_spec.yaml` describing
   what the skill should do. Run `--from-spec` to generate both a complete SKILL.md
   (with frontmatter, sections, examples) and a matching `task_suite.yaml`.
3. **Full lifecycle** -- Generate a skill, test it with `--evaluate`, and optionally
   improve it with `--auto-improve` in one pass. Combines skill-forge,
   improvement-evaluator, and improvement-orchestrator into a single command.
4. **Validate coverage of an existing suite** -- Compare the generated task_suite
   against a hand-written one to find untested scenarios.

## When NOT to Use

- You just want to **evaluate** an existing skill with an existing `task_suite.yaml`
  → use `improvement-evaluator`
- You just want to **improve** a skill that already has tests
  → use `improvement-orchestrator`
- You want to **manually write** a SKILL.md with templates
  → use `skill-creator`
- You want to **score improvement candidates** (not generate tests)
  → use `improvement-discriminator`
- You want to **merge overlapping skills** into one consolidated skill
  → use `skill-distill`

## Modes

### Mode A: `--from-skill` (Generate task suite for existing SKILL.md)

```bash
# Generate test suite for an existing skill
python3 scripts/forge.py --from-skill /path/to/skill-dir --output /path/to/output

# Generate and immediately evaluate
python3 scripts/forge.py --from-skill /path/to/skill-dir --output /path/to/output --evaluate
```

Reads the SKILL.md, extracts scenarios from five sources in priority order:

1. **Frontmatter** (description, triggers) → 1 core-capability test
2. **"When to Use" bullets** → up to 3 positive use-case tests
3. **`<example>` tags** → up to 2 keyword-match tests (uses `ContainsJudge`)
4. **`<anti-example>` tags** → up to 2 negative tests (should avoid bad patterns)
5. **Output format/CLI sections** → 1 format compliance test

Produces `task_suite.yaml` in the output directory. Example generated output:

```yaml
skill_id: release-notes-generator
version: "1.0"
generated_by: skill-forge
tasks:
  - id: release-notes-generator-core-capability
    description: "Test core capability described in skill description"
    prompt: "You are an AI assistant with this skill loaded..."
    judge:
      type: llm-rubric
      rubric: "The output should demonstrate the capability..."
      pass_threshold: 0.7
    timeout_seconds: 120
    source: frontmatter.description
  - id: release-notes-generator-use-case-01
    description: "Use case: Generate notes from git log between tags"
    prompt: "Scenario: Generate notes from git log..."
    judge:
      type: llm-rubric
      rubric: "The output should address this use case..."
      pass_threshold: 0.6
    timeout_seconds: 120
    source: when_to_use
```

### Mode B: `--from-spec` (Generate skill + task suite from spec)

```bash
# Generate complete skill from a spec file
python3 scripts/forge.py --from-spec spec.yaml --output /path/to/output

# Generate, evaluate, and auto-improve if below SOLID grade
python3 scripts/forge.py --from-spec spec.yaml --output /path/to/output --auto-improve
```

Reads a `skill_spec.yaml` (see `references/spec-format.md`) and generates:

1. A complete SKILL.md with frontmatter, When to Use / When NOT to Use, examples, output format
2. A `task_suite.yaml` derived from the generated SKILL.md (same five-source extraction)

The spec format requires only `name` and `purpose`; optional fields (`inputs`, `outputs`, `quality_criteria`, `domain_knowledge`, `reference_skills`) enrich the generated SKILL.md. Example minimal spec:

```yaml
name: release-notes-generator
purpose: Generate structured release notes from git commit history

inputs:
  - name: commits
    type: git-log
    description: "Git commit log between two tags"

outputs:
  - name: release-notes
    format: markdown
    description: "Structured release notes with sections"

quality_criteria:
  - name: completeness
    description: "All commits accounted for in the notes"
    weight: 0.3
```

### Common Flags

| Flag | Effect |
|------|--------|
| `--mock` | Use mock LLM (for testing without API calls) |
| `--evaluate` | Run `improvement-evaluator` after generation (requires it installed) |
| `--auto-improve` | Run `improvement-orchestrator` if score below SOLID (requires it installed) |

## Output Artifacts

| Request | Deliverable | Location |
|---------|------------|----------|
| `--from-skill` | `task_suite.yaml` with 5-10 test tasks | `<output>/task_suite.yaml` |
| `--from-spec` | `SKILL.md` + `task_suite.yaml` | `<output>/<name>/SKILL.md`, `<output>/<name>/task_suite.yaml` |
| `--evaluate` | Evaluation report (pass/fail per task, aggregate pass rate) | stdout + `<output>/evaluation_report.json` |
| `--auto-improve` | Improved SKILL.md (if score was below SOLID) | in-place update of `SKILL.md` |

All generated YAML files use `allow_unicode: True` and `default_flow_style: False` for human readability. Files are written atomically (write-then-rename) to prevent corruption on crash.

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

## Why Null-Skill Calibration

A generated task suite is only useful if it measures the _skill's_ contribution, not the base LLM's general ability. Without calibration, a naive suite can report 80%+ pass rates even when the SKILL.md adds zero value -- because the LLM already knows how to answer those questions.

**Null-skill calibration** addresses this by running every candidate task against a "null skill" (empty context, no SKILL.md loaded). Any task the null skill passes trivially is filtered out before the final suite is emitted. This ensures that every surviving task genuinely requires the knowledge or structure encoded in the SKILL.md.

**Tradeoff**: Null-skill calibration adds one extra LLM call per candidate task (or a heuristic keyword check in `--mock` mode). For a typical 10-task candidate set, this means ~10 additional calls during suite generation. The cost is justified because an uncalibrated suite gives false confidence: a skill that scores 9/10 on easy tasks looks "SOLID" but may add no value over a bare model. Calibrated suites reliably distinguish genuine skill contributions from baseline LLM capability.

When `--mock` is used, calibration falls back to a heuristic: tasks whose prompt contains only generic verbs ("explain", "describe", "list") without skill-specific terminology are filtered. This is less precise than LLM-based calibration but costs zero API calls.

The calibration step runs after deduplication and before the final cap of 10 tasks per suite.

## Related Skills

| Skill | Relationship | When to prefer over skill-forge |
|-------|-------------|-------------------------------|
| `improvement-evaluator` | Downstream consumer: runs the generated `task_suite.yaml` and reports pass/fail per task | You already have both SKILL.md and task_suite.yaml, just need to run them |
| `improvement-orchestrator` | Drives the full generate-evaluate-improve loop; skill-forge is one step in this loop | You want automatic multi-round improvement, not just test generation |
| `improvement-generator` | Generates improvement candidates (patches) for a SKILL.md | You want to improve an existing skill's prose/structure, not generate tests |
| `improvement-discriminator` | Scores improvement candidates via multi-reviewer blind panel | You need to judge which candidate patch is best |
| `skill-creator` | Manual SKILL.md authoring guide with templates | You prefer hand-writing the SKILL.md rather than generating it |
| `skill-distill` | Merges multiple overlapping skills into one distilled skill | You have redundant skills to consolidate, not a new skill to create |
