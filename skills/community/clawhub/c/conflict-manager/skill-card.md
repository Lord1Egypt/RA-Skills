## Description:

Provides HTTP endpoints for scanning Git repository conflicts across branches, applying AI-suggested resolutions, and publishing related WebSocket events.

This skill is ready for commercial/non-commercial use.

## Publisher:

[brajesh9373](https://clawhub.ai/user/brajesh9373)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering teams use this skill to let a dashboard request repository conflict scans and apply proposed conflict resolutions across source and target branches.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Repository write access could allow merges or pushes to important branches without clear safeguards.

Mitigation: Require explicit user approval before any non-dry-run resolution and restrict which repositories and branches the skill can modify.

Risk: Resolution payloads may include command lists that could be unsafe if accepted without controls.

Mitigation: Avoid arbitrary command lists unless they are tightly constrained, reviewed, and audited.

Risk: Public HTTP endpoints for conflict scan and resolution behavior need defined access controls.

Mitigation: Define authentication and audit behavior before deployment.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/brajesh9373/skills/conflict-manager)
- [ClawHub Publisher Profile](https://clawhub.ai/user/brajesh9373)

## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [JSON responses and WebSocket event payloads]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May involve repository write operations when non-dry-run resolution is used.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
