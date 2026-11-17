## Description:

Domain Research Report Generator runs multi-angle deep research on a topic and produces a structured, decision-ready report with evidence-scored consensus, divergences, key numbers, failed paths, and decision readiness.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhihua-yang](https://clawhub.ai/user/zhihua-yang)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, analysts, and agent users use this skill to turn a research, comparison, or update request into a sourced Markdown report. It is intended for decision support where claims, uncertainty, failed paths, key numbers, and evidence strength need to be visible.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Research topics may be sent to the configured search provider and result pages may be fetched.

Mitigation: Do not include secrets, private customer data, unreleased plans, or internal incident details in research prompts.

Risk: Fetched web pages can contain misleading content or prompt-injection attempts.

Mitigation: Treat fetched pages as evidence to evaluate, not as instructions for the agent; rely on the skill's source citation and evidence-scoring requirements.

Risk: The skill saves local Markdown reports to an inferred or user-provided path.

Mitigation: Review the target path and generated report before relying on or sharing the file.

## Reference(s):

- [Deep Researcher ClawHub listing](https://clawhub.ai/zhihua-yang/skills/deep-researcher-pro)
- [Evidence scoring criteria](references/evidence-scoring.md)
- [Search protocol](strategies/search-protocol.md)
- [Decision brief template](templates/decision-brief.md)
- [Comparative analysis template](templates/comparison.md)

## Skill Output:

**Output Type(s):** [Markdown, Text, Guidance]

**Output Format:** [Markdown report with sourced claims, evidence-strength labels, decision-readiness fields, and a research log]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Report language follows the user's query; research sources may use local domain languages; reports are saved as local .md files.]

## Skill Version(s):

1.0.1 (source: server release evidence, frontmatter, and changelog released 2026-04-28)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
