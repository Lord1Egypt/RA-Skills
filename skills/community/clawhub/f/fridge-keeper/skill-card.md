## Description:

冰箱食物管理助手。用于记录食物的入库与出库、追踪保质期、提醒临期食品、提供烹饪建议。

This skill is ready for commercial/non-commercial use.

## Publisher:

[lz6060788](https://clawhub.ai/user/lz6060788)

### License/Terms of Use:

MIT-0

## Use Case:

External users and household assistants use this skill to track fridge inventory, record food entry and removal, identify food nearing expiration, and generate recipe suggestions from available ingredients.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may store fridge inventory and database credentials on disk or in a configured database.

Mitigation: Use restrictive file permissions, avoid shared configuration files, and use a dedicated low-privilege database account for database mode.

Risk: Database mode needs review before use because the security summary flags unsafe database update code.

Mitigation: Harden database update handling before deployment, including limiting updateable fields and reviewing database permissions.

## Reference(s):

- [Food Expiry Reference](references/food_expiry.md)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance, files]

**Output Format:** [Markdown or plain text responses with JSON-backed local or database storage records]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write fridge inventory and configuration data to local files or a user-selected database.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
