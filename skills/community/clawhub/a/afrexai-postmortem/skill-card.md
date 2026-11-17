## Description:

Generates structured, blameless incident postmortems from raw incident notes, Slack threads, bullet points, verbal notes, or PagerDuty alerts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[1kalin](https://clawhub.ai/user/1kalin)

### License/Terms of Use:


## Use Case:

Incident responders, SREs, and engineering teams use this skill to turn rough incident material into draft postmortems with an executive summary, timeline, root cause analysis, impact assessment, action items, lessons learned, and prevention measures.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Users may paste sensitive incident details, secrets, tokens, customer personal data, private Slack content, or regulated information into the skill.

Mitigation: Install only in an approved environment and redact sensitive or regulated information unless the organization allows that data to be processed by the agent.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/1kalin/skills/afrexai-postmortem)
- [AfrexAI Context Packs](https://afrexai-cto.github.io/context-packs/)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown postmortem draft with structured sections, action items, flagged gaps, and ranked prevention measures.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses blameless language, ISO timestamps, severity labels, owner and deadline placeholders, and priority tags.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
