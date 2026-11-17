## Description:

Run a blameless postmortem for an incident caused by an AI agent or LLM feature, producing trace reconstruction, layered root-cause analysis, and corrective actions with a permanent regression case.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mohitagw15856](https://clawhub.ai/user/mohitagw15856)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, operators, and incident reviewers use this skill to investigate AI agent or LLM feature incidents such as hallucinated facts, prompt injection effects, runaway tool use, cost blowouts, or incorrect autonomous actions. It helps produce a blameless postmortem that reconstructs the trace, identifies the earliest preventable failure layer, and records corrective actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Incident traces may contain credentials, tokens, personal data, confidential documents, or unrelated system details.

Mitigation: Provide only incident-relevant excerpts when possible and redact sensitive or unrelated information before sharing traces with the skill.

Risk: Permanent regression cases can preserve sensitive incident content if built from raw traces.

Mitigation: Use sanitized or synthetic traces for permanent regression cases.

## Reference(s):

- [Agent Incident Postmortem homepage](https://mohitagw15856.github.io/pm-claude-skills/skill/agent-incident-postmortem.html)
- [ClawHub skill page](https://clawhub.ai/mohitagw15856/skills/agent-incident-postmortem)

## Skill Output:

**Output Type(s):** [Markdown, Analysis, Guidance]

**Output Format:** [Markdown postmortem document with tables and checklists]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes timeline, impact summary, trace reconstruction, layered root-cause findings, reproduction notes, corrective actions, and quality checks.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
