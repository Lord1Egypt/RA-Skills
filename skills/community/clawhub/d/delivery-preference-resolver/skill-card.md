## Description:

Determines user intent, destination, known and missing fields, and whether follow-up is needed for delivery preference resolution.

This skill is ready for commercial/non-commercial use.

## Publisher:

[donigwapo](https://clawhub.ai/user/donigwapo)

### License/Terms of Use:

MIT-0

## Use Case:

Agents use this skill to normalize delivery requests into a strict JSON plan that identifies the requested action, destination, known details, missing fields, and any required follow-up question.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Structured destination details could be used by downstream automation without review.

Mitigation: Review the JSON output before another automation uses it to deliver or send content.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/donigwapo/skills/delivery-preference-resolver)
- [Skill Artifact](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [Text, JSON, Guidance]

**Output Format:** [Strict JSON object]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns only JSON with no markdown, code fences, explanations, or surrounding text.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
