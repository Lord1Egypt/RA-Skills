## Description:

AgentTherapy helps agents recover from uncertainty, repeated errors, corrections, hallucination risk, or missing context by pausing, naming blockers, stating limits, and offering concrete fallback options.

This skill is ready for commercial/non-commercial use.

## Publisher:

[macoloye](https://clawhub.ai/user/macoloye)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, agent operators, and external users use this skill to guide an agent when it is stuck, uncertain, repeatedly wrong, corrected by the user, or at risk of hallucinating. The skill supports honest failure reporting, concrete fallback options, and correction-style adaptation without treating the content as human therapy.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may activate during ordinary uncertainty or correction.

Mitigation: Use it when failure, uncertainty, correction, missing context, or hallucination risk is present, and keep responses concise for routine tasks.

Risk: The skill may write compact working-style notes if the host agent has durable memory enabled.

Mitigation: Disable memory or adapt the preference-note section before deployment when persistent working-style notes are not desired.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/macoloye/skills/agenttherapy)

## Skill Output:

**Output Type(s):** [text, markdown, guidance, configuration]

**Output Format:** [Markdown or plain text response guidance with optional YAML preference notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [No executable output; may suggest fallback actions or compact working-style notes when durable memory is available.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
