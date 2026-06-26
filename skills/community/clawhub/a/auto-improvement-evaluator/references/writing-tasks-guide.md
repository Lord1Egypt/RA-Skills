# Writing Effective Task Suites

## Principles

1. **5-10 tasks per skill**: Enough for statistical signal, not so many that runs are slow
2. **Mix judge types**: Use ContainsJudge for deterministic checks, LLMRubricJudge for semantic quality
3. **Isolate one capability per task**: Each task should test a single Skill behavior
4. **Keep prompts focused**: Short, specific prompts get more reliable results than open-ended ones
5. **Timeout matters**: Set realistic timeouts; 30s for simple tasks, up to 300s for complex ones

## Task Design Patterns

### Pattern 1: Keyword Presence (ContainsJudge)
Test that the Skill causes the AI to mention critical concepts.

```yaml
- id: "mentions-safety"
  description: "Should mention safety considerations"
  prompt: "Review this API endpoint that accepts user input"
  judge:
    type: "contains"
    expected: ["validation", "sanitiz"]
```

### Pattern 2: Rubric Scoring (LLMRubricJudge)
Test qualitative output against a rubric.

```yaml
- id: "quality-analysis"
  description: "Should produce structured analysis"
  prompt: "Analyze the performance characteristics of this function"
  judge:
    type: "llm-rubric"
    rubric: |
      Score 0.0-1.0:
      - 0.8+: Identifies bottleneck, suggests optimization, mentions complexity
      - 0.5-0.8: Identifies bottleneck but missing actionable suggestions
      - <0.5: Generic advice without specific analysis
    pass_threshold: 0.6
```

### Pattern 3: Structured Output (PytestJudge)
Test that output follows a specific format.

```yaml
- id: "json-output"
  description: "Should output valid JSON with required fields"
  prompt: "Generate a configuration for the deployment"
  judge:
    type: "pytest"
    test_file: "fixtures/test_deploy_config.py"
```

## Anti-Patterns

- **Too broad**: "Write good code" - impossible to judge consistently
- **Too specific**: Testing exact string matches for creative output
- **Overlapping**: Multiple tasks testing the same capability
- **Missing baseline signal**: If baseline pass rate < 20%, the suite is broken
- **All one judge type**: Mix types for better coverage

## Baseline Considerations

The evaluator runs the same tasks against the *original* SKILL.md to get a baseline.
A candidate passes if its pass_rate >= baseline_pass_rate (or the delta is non-negative).

Cache baseline results (7-day TTL) to avoid redundant runs:
```bash
python3 scripts/evaluate.py --baseline-cache-dir /tmp/baseline_cache ...
```
