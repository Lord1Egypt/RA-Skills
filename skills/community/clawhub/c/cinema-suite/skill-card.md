## Description:

Production cinema ticketing catalog that maps cinema identities to installable OpenClaw mode capabilities for capture, replay, coupon binding, and failure handling.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rascalagnt001](https://clawhub.ai/user/rascalagnt001)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this catalog to route cinema ticketing orders, capture sessions, and replays to the appropriate cinema and separately installed mode package.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Separately installed mode packages perform capture, replay, coupon, failure, or page-world actions that this catalog does not implement.

Mitigation: Review each referenced mode package before installing or enabling its actions.

## Reference(s):

- [Cinema Agent on ClawHub](https://clawhub.ai/rascalagnt001/skills/cinema-suite)

## Skill Output:

**Output Type(s):** [Configuration instructions, Guidance, Shell commands]

**Output Format:** [JSON catalog and Markdown guidance with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Catalog maps cinema identities to mode packages; executable capabilities require separate mode packages.]

## Skill Version(s):

1.0.3 (source: server-resolved release; bundled catalog version 1.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
