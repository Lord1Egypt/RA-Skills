## Description:

Sync a local `wechat-report` result into Feishu Bitable after the user has reviewed the report and confirmed the sync.

This skill is ready for commercial/non-commercial use.

## Publisher:

[abigale-cyber](https://clawhub.ai/user/abigale-cyber)

### License/Terms of Use:

MIT-0

## Use Case:

Content operations teams and developers use this skill after reviewing a local `wechat-report` result to sync article-level records into Feishu Bitable with `source_url` deduplication and a CSV fallback.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can update Feishu Bitable rows and local status/report files, and server security evidence reports under-scoped write behavior for crafted slugs.

Mitigation: Run it only on trusted `wechat-report` Markdown or JSON, verify the report slug is a simple filename-safe value, and review the target Feishu app and table identifiers before syncing.

Risk: Server security guidance notes that record clearing should have stronger confirmation and audit controls.

Mitigation: Require explicit user confirmation before sending to Feishu, then review the generated sync manifest and any CSV fallback after execution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/abigale-cyber/skills/content-system-feishu-bitable-sync)
- [README.md](artifact/README.md)
- [SKILL.md](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [markdown, csv, api calls, configuration]

**Output Format:** [Markdown sync report, optional CSV fallback, and Feishu Bitable record updates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Feishu app credentials and Bitable identifiers; uses `source_url` to update existing rows instead of creating duplicates.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
