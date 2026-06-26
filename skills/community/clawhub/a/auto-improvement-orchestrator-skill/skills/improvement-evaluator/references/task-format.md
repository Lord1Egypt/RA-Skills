# Task Suite Format

Task suites are YAML files that define a set of tasks to evaluate a Skill's execution effectiveness.

## Schema

```yaml
skill_id: "target-skill-name"     # Required: which skill this suite tests
version: "1.0"                     # Required: suite schema version
tasks:                             # Required: list of tasks (5-10 recommended)
  - id: "unique-task-id"          # Required: unique within suite
    description: "What this tests" # Required: human-readable
    prompt: "The prompt text"      # Required: sent to claude -p with SKILL.md prepended
    judge:                         # Required: how to evaluate the output
      type: "contains"             # Required: contains | pytest | llm-rubric
      # type-specific fields below
    timeout_seconds: 30            # Optional: per-task timeout (default: 300)
```

## Judge Types

### ContainsJudge
Checks that all expected keywords appear in the output (case-insensitive).

```yaml
judge:
  type: "contains"
  expected: ["keyword1", "keyword2"]
```

### PytestJudge
Runs a pytest test file against the AI output. The output is written to a temp file
and its path is available via the `AI_OUTPUT_FILE` environment variable.

```yaml
judge:
  type: "pytest"
  test_file: "fixtures/test_output_format.py"  # Must start with fixtures/
```

### LLMRubricJudge
Uses an LLM to score the output against a rubric. Supports `--mock` mode for testing.

```yaml
judge:
  type: "llm-rubric"
  rubric: "Score based on: 1) correctness 2) completeness 3) clarity"
  pass_threshold: 0.7  # 0.0-1.0, default 0.7
```

## Validation Rules

1. `skill_id` must be non-empty
2. `version` must be "1.0"
3. Each task must have a unique `id`
4. `prompt` must be non-empty
5. `judge.type` must be one of: contains, pytest, llm-rubric
6. For contains: `expected` must be a non-empty list of strings
7. For pytest: `test_file` must start with "fixtures/"
8. For llm-rubric: `rubric` must be non-empty

## Example

```yaml
skill_id: "benchmark-store"
version: "1.0"
tasks:
  - id: "bs-quality-tier-01"
    description: "Should identify correct quality tier"
    prompt: "Given these scores {accuracy: 0.9, coverage: 0.85}, what quality tier?"
    judge:
      type: "contains"
      expected: ["POWERFUL"]
    timeout_seconds: 30

  - id: "bs-explain-regression"
    description: "Should explain Pareto front regression"
    prompt: "A skill's accuracy dropped from 0.9 to 0.8 but coverage went up. Accept?"
    judge:
      type: "llm-rubric"
      rubric: "Must mention trade-off analysis and provide a clear recommendation"
      pass_threshold: 0.7
```
