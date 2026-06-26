# Experiment Design Methodology

> Distilled from real-world controlled experiment design practice

## Progressive Building

Never build everything at once. The minimum loop:

```
Minimum artifact set → schema validation → small task set → baseline+treatment dry run → scoring → error analysis
```

Only after this loop produces distinguishable scores should you expand to full scale. The principle is: if you cannot detect a signal with 5 tasks, you will not detect it with 50.

## Controlled Group Design

The goal is **attributable causality** — knowing which variable caused the observed difference.

| Group | Name | Input | Purpose |
|-------|------|-------|---------|
| Baseline | No augmentation | User task only | Does the model's internal knowledge suffice? |
| Treatment A | Unstructured input | Task + raw text/documents | Test basic augmentation |
| Treatment B | Structured input | Task + structured artifacts | Core test: does structure matter? |
| Treatment C | Full context | Task + artifacts + constraints + metadata | Attribution: what does the extra layer add? |

**Attribution principle**: Adjacent groups differ by exactly one variable. This lets you say "the difference between Treatment B and Baseline is caused by structured input," not "something in the setup changed."

## Output Format Contract

Define the agent's output as a strict schema (YAML or JSON) with required fields. The scorer and downstream analysis depend on this contract. Changing the schema requires a version bump and re-validation.

Example structure (adapt to your domain):

```yaml
# Required: what the task asks for
goal_summary: str

# Required: core output content (domain-specific)
key_findings: list[{name, description, rationale}]
methodology: list[{step_id, description, inputs, outputs}]
constraints: list[{type, description, mitigation}]

# Required: provenance
evidence: list[str]        # references to knowledge artifacts
citations: list[str]       # external references

# Optional: meta
risk_notes: list[str]
confidence: str            # high | medium | low
```

The exact fields depend on your domain. The critical rule: **the schema is a contract** between the runner, the scorer, and the analysis pipeline. All three must agree on it.

## Gold Checklist Per Task

Every task needs explicit ground truth for evaluation:

```yaml
task_type: str
must_include:
  - category: items the output must contain
forbidden:
  - "known bad pattern that should not appear"
scoring_notes:
  - "partial credit rules and edge cases"
```

The checklist serves two purposes:
1. **Coverage scoring**: what fraction of must_include items appear in the output?
2. **Negative filtering**: forbidden patterns penalize the score

## Knowledge Artifact Schema

If your experiment injects structured knowledge into the agent, each artifact should answer four planning questions:

- **Trigger**: When is this knowledge recalled?
- **Constraint**: What does it constrain or limit?
- **Connection**: What other artifacts, concepts, or tools does it relate to?
- **Verification**: How is its correctness established?

Plus evidence tracking:
- **evidence_type**: primary_source | secondary_source | ai_generated | expert_opinion
- **confidence_level**: high | medium | low
- **review_status**: verified | candidate | needs-review | rejected

The review_status field is critical: `rejected` artifacts remain in the registry to prevent the agent from rediscovering and reusing bad candidates.

## Execution Sequence

1. **Dry run**: print prompt, no API call — verify prompt construction
2. **Smoke run**: 1 task × 2 groups — verify output parsing and schema compliance
3. **Wave 1**: small task set × all groups — minimum viable data for signal detection
4. **Wave 2**: expanded task set — coverage and generalization
5. **Wave 3**: ablation analysis + visualization

## Preflight Gate

Before ANY formal run:
```bash
python scripts/validate_tasks.py
python scripts/validate_scoring.py
python scripts/validate_results_manifest.py
python scripts/validate_repo_state.py
```

Expected: all PASS, 0 FAIL.
