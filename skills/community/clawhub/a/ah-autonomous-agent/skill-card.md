## Description:

Autonomous Agent guides an agent through goal-directed planning, adaptive learning, and self-correction with minimal human supervision.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mtsatryan](https://clawhub.ai/user/mtsatryan)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to structure autonomous work such as feature implementation, optimization, research, and recovery while maintaining escalation boundaries for high-risk decisions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad autonomy language could encourage an agent to act with less supervision than the deployment policy allows.

Mitigation: Keep normal approval controls enabled for production, destructive, security-sensitive, privacy-impacting, financial, and long-running work.

Risk: The skill describes learning and self-correction patterns but does not provide a real memory or automation implementation.

Mitigation: Treat learning, metrics, and self-correction language as operational guidance that still requires external validation and review.

## Reference(s):

- [Autonomous Agent examples](references/examples.md)
- [ClawHub skill page](https://clawhub.ai/mtsatryan/skills/ah-autonomous-agent)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with structured plans, checklists, tables, and inline code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces guidance for autonomous planning, execution tracking, escalation, and self-review; it does not implement persistence, credentials, or hidden execution.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
