## Description:

Feishu Bitable Data Sync helps an agent synchronize data between Feishu Bitables or import data from external sources.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ramlee77](https://clawhub.ai/user/ramlee77)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and automation users use this skill to guide one-way or two-way Feishu Bitable sync workflows, including listing tables, reading records, importing external data, and preparing create, update, or delete record operations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Bulk sync operations can create, update, or delete live Feishu Bitable records.

Mitigation: Require a preview or explicit confirmation before create, update, or delete operations.

Risk: Incorrect app_token, table_id, or field type mappings can target the wrong table or produce malformed record changes.

Mitigation: Verify exact app_token and table_id values and confirm field types match before running a sync.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ramlee77/skills/feishu-bitable-sync)

## Skill Output:

**Output Type(s):** [guidance, configuration, API calls, JSON]

**Output Format:** [Markdown guidance with JSON request examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs rely on user-provided Feishu app_token and table_id values and matching field schemas.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
