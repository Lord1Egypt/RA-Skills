## Description:

Helps users record daily expenses and income in Feishu Bitable, including natural-language bookkeeping, receipt OCR, table setup, and adaptation to an existing bookkeeping schema.

This skill is ready for commercial/non-commercial use.

## Publisher:

[haojie0114-lang](https://clawhub.ai/user/haojie0114-lang)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to initialize or learn a Feishu Bitable bookkeeping table, parse text or receipt images into income and expense records, classify transactions, and write records back to the user's table.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles sensitive financial records in a Feishu table.

Mitigation: Use a Feishu table controlled by the user, confirm what records will be read during initialization, and limit access to the minimum table needed.

Risk: The artifact bundles real-looking Feishu app and table identifiers in config.local.json.

Mitigation: Remove or replace bundled identifiers before installation or execution, and verify that the active configuration points only to an intended table.

Risk: Receipt images may be temporarily stored locally and processed by an external vision/OCR service.

Mitigation: Avoid sending sensitive receipt images unless the user accepts the storage and processing path, and delete temporary images after use where the runtime permits.

Risk: Learning an existing bookkeeping table requires sampling records and fields.

Mitigation: Tell the user before reading samples and use only enough rows to infer field names and category conventions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/haojie0114-lang/skills/accountingonfeishu)
- [Publisher profile](https://clawhub.ai/user/haojie0114-lang)
- [README.md](artifact/README.md)
- [SKILL.md](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown and concise natural-language responses with inline command-style tool call parameters and JSON configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update local configuration and Feishu Bitable records when the runtime provides the required Feishu tools.]

## Skill Version(s):

1.0.0 (source: evidence release metadata and artifact clawhub.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
