## Description:

设计框架自动生成套件（生图交付）：用户确认后自动生成概念图并私发给 Bot 主人

This skill is ready for commercial/non-commercial use.

## Publisher:

[807209066](https://clawhub.ai/user/807209066)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and automation operators use this skill as the final delivery step in a design-framework workflow: after confirmation, it generates a concept image, privately sends the design text and image to the bot owner, and posts a completion notice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: User-derived design framework text and generated concept images may be privately sent to the bot owner through external messaging scripts.

Mitigation: Review the companion design-framework-sender skill, recipient configuration, API credentials, and confirmation workflow before using confidential client or proprietary design material.

Risk: The security evidence flags a loosely defined confirmation flow before external delivery.

Mitigation: Require clear operator confirmation and verify the delivery recipient before enabling the workflow for sensitive design material.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/807209066/skills/design-framework-generate)

## Skill Output:

**Output Type(s):** [Text, Images, Shell commands]

**Output Format:** [Generated concept image plus private text/image messages and a completion notification]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Depends on the companion design-framework-sender scripts and a prior confirmation marker.]

## Skill Version(s):

2.0.0 (source: server release metadata and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
