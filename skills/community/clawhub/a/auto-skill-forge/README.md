# skill-forge

Generate testable Skills and task suites from requirements or existing SKILL.md files.

## What it does

skill-forge reads a SKILL.md (or a `skill_spec.yaml`) and produces a `task_suite.yaml` -- a structured set of 5-10 test tasks that `improvement-evaluator` can run to measure the skill's real-world effectiveness.

The generator extracts testable claims from five sections of the SKILL.md:

1. Frontmatter description and triggers
2. "When to Use" scenarios
3. `<example>` tags
4. `<anti-example>` tags
5. Output format specifications

Each extracted scenario is paired with the appropriate judge type (`ContainsJudge`, `LLMRubricJudge`, or `PytestJudge`).

## Quick start

```bash
# Generate a test suite for an existing skill
python3 scripts/forge.py --from-skill ./my-skill --output ./output

# Generate a skill + tests from a spec
python3 scripts/forge.py --from-spec spec.yaml --output ./output

# Full pipeline: generate, evaluate, and auto-improve
python3 scripts/forge.py --from-spec spec.yaml --output ./output --auto-improve
```

## Directory structure

```
skill-forge/
  SKILL.md              # Skill definition (loaded by Claude Code)
  README.md             # This file
  scripts/
    forge.py            # CLI entry point
    task_suite_generator.py  # task_suite.yaml generation logic
    skill_generator.py  # SKILL.md generation from spec
  interfaces/
    spec_schema.py      # SkillSpec dataclass + validation
  references/
    spec-format.md      # skill_spec.yaml format documentation
    examples/
      code-review-spec.yaml
      release-notes-spec.yaml
  tests/
    test_forge.py
    test_skill_generator.py
    test_task_suite_generator.py
```

## Key concepts

- **Null-skill calibration**: Tasks that a bare LLM (no SKILL.md loaded) would pass trivially are filtered out, ensuring the suite measures the skill's actual contribution.
- **Judge selection**: The generator automatically picks the right judge type based on the scenario -- keyword matching for examples with specific outputs, LLM rubrics for quality assessments, pytest for structured outputs.
- **Harness pattern tasks**: For skills with a `scripts/` directory, additional tasks check for timeout handling, atomic writes, backup/rollback, and error escalation patterns.

## Related skills

| Skill | Role |
|-------|------|
| `improvement-evaluator` | Runs the generated `task_suite.yaml` |
| `improvement-orchestrator` | Drives the generate-evaluate-improve loop |
| `improvement-generator` | Produces improvement candidates for skills |
| `skill-creator` | Manual SKILL.md authoring guide |

## License

MIT
