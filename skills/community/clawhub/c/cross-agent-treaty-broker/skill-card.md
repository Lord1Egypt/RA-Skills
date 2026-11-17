## Description:

Local inter-agent treaty negotiation with consent loops.

This skill is ready for commercial/non-commercial use.

## Publisher:

[deepseekoracle](https://clawhub.ai/user/deepseekoracle)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators of multi-agent workflows use the skill to draft, review, record, list, revoke, and inspect proposed agreements for data sharing and agent capabilities.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Crafted treaty files can overwrite other JSON files.

Mitigation: Use trusted treaty files in an isolated directory with disposable records until path-containment safeguards are verified.

Risk: Routine commands can erase audit anchors.

Mitigation: Do not rely on audit history until anchor-preservation safeguards are verified; evaluate only with disposable records.

Risk: Promised confirmation checks are missing.

Mitigation: Wait for confirmation safeguards before relying on the skill for consent or auditing.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/deepseekoracle/skills/cross-agent-treaty-broker)
- [Quick Start](references/quick-start.md)
- [Treaty JSON Schema](references/treaty-json-schema.json)

## Skill Output:

**Output Type(s):** [JSON, Text, Shell commands]

**Output Format:** [JSON treaty documents and plain-text previews or command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Treaty records and previews are organized around individual treaty IDs.]

## Skill Version(s):

2.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
