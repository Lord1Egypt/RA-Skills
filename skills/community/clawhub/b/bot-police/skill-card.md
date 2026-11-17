## Description:

Detect, investigate, and contain malicious or compromised bots using behavior analysis, policy enforcement, and escalation protocols.

This skill is ready for commercial/non-commercial use.

## Publisher:

[arhadnane](https://clawhub.ai/user/arhadnane)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators of multi-bot systems use this skill to score bot behavior, flag malicious indicators, and recommend watch, block, or quarantine actions for incident triage.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can recommend block or quarantine actions without clear user-control boundaries.

Mitigation: Scope bot restriction and quarantine permissions explicitly and require human approval before disruptive containment actions.

Risk: Malformed or untrusted telemetry can manipulate behavior scoring.

Mitigation: Validate telemetry schemas and trust sources before using the skill's scores or containment recommendations.

## Reference(s):

- [Bot Police ClawHub Skill Page](https://clawhub.ai/arhadnane/skills/bot-police)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Structured incident-triage guidance with behavior scores, flagged bots, containment recommendations, and summary counts.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Recommendations should be treated as advisory unless telemetry is trusted and schema-validated.]

## Skill Version(s):

1.0.0 (source: release evidence, artifact/skill.json, index.js)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
