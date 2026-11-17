## Description:

飞书多维表格（Bitable）的创建、查询、编辑和管理工具，包含 27 种字段类型支持、高级筛选、批量操作和视图管理。

This skill is ready for commercial/non-commercial use.

## Publisher:

[a3152557994-ship-it](https://clawhub.ai/user/a3152557994-ship-it)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to create and manage Feishu Bitable apps, tables, fields, views, records, filters, batch operations, and attachment workflows. It is intended for workflows that need structured guidance for reading, writing, importing, updating, and deleting Bitable data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide writes, deletes, batch operations, schema changes, and attachment uploads that persist changes to Feishu Bitable business data.

Mitigation: Before executing those actions, confirm the exact app_token, table_id, records, fields, action, and file contents with the user.

Risk: Delete operations may not be recoverable and default tables can contain empty records that pollute later imports.

Mitigation: Review target record IDs before deletion and list records first when cleaning default table rows before importing data.

Risk: Incorrect field value formats can cause failed writes or malformed records, especially for people, dates, select fields, URLs, and attachments.

Mitigation: List field metadata before writing records, match each value to its field type, and use the bundled record value and field property references for validation.

## Reference(s):

- [字段 Property 配置详解](references/field-properties.md)
- [记录值数据结构详解](references/record-values.md)
- [使用场景完整示例](references/examples.md)
- [飞书开放平台 - 字段编辑指南](https://go.feishu.cn/s/672BSzVyo03)
- [飞书开放平台 - 多维表格记录数据结构](https://go.feishu.cn/s/6lY28723w04)
- [飞书开放平台 - 多维表格文档](https://open.feishu.cn/document/server-docs/docs/bitable-v1/bitable-overview)

## Skill Output:

**Output Type(s):** [guidance, markdown, code, configuration]

**Output Format:** [Markdown guidance with JSON request examples and parameter notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include Feishu Bitable tool names, action names, field schemas, record value formats, filters, batch-operation constraints, and troubleshooting guidance.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
