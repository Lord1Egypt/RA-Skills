## Description:

Coordinates a full skill-improvement pipeline that proposes candidates, scores them, optionally evaluates them, executes supported changes, gates the result, and retries failed improvements with trace-aware feedback.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lanyasheng](https://clawhub.ai/user/lanyasheng)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and skill maintainers use this skill to run an end-to-end improvement cycle for one or more agent skills, including candidate generation, scoring, optional evaluation, execution, gate review, retry traces, and state artifacts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can automatically modify skill files.

Mitigation: Run it only in a version-controlled or disposable workspace, use explicit target and state directories, and review generated diffs and state artifacts before keeping changes.

Risk: Validation and scoping controls are reported as loose.

Mitigation: Limit targets to intended skill directories, inspect pipeline artifacts, and require human review for medium-risk, high-risk, protected-target, or non-documentation changes.

Risk: Evaluator failures may not block execution.

Mitigation: Do not rely on evaluator failure as the only gate; review gate receipts and treat failed or missing evaluation evidence as requiring manual approval.

## Reference(s):

- [Architecture](references/architecture.md)
- [Guardrails](references/guardrails.md)
- [Phases](references/phases.md)
- [Adapters](references/adapters.md)
- [Skill-Evaluator Adapter](references/skill-evaluator-adapter.md)
- [End-to-End Demo](references/end-to-end-demo.md)
- [ClawHub Skill Page](https://clawhub.ai/lanyasheng/skills/auto-improvement-orchestrator)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown instructions, shell commands, and JSON pipeline artifacts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes local state artifacts such as candidate versions, rankings, execution records, receipts, traces, and pipeline-summary.json.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata; artifact frontmatter says 0.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
