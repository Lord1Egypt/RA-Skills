## Description: <br>
飞书多维表格（Bitable）的创建、查询、编辑和管理工具，包含 27 种字段类型支持、高级筛选、批量操作和视图管理。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[a3152557994-ship-it](https://clawhub.ai/user/a3152557994-ship-it) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to create, query, update, and manage Feishu Bitable apps, tables, fields, views, and records. It is especially useful for batch imports, schema-sensitive record updates, and troubleshooting common Bitable field-format errors. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill guides agents through data-changing Feishu Bitable operations, including bulk updates and deletes. <br>
Mitigation: Use least-privilege Feishu access, confirm the target app and table before changes, and review bulk update or delete requests before execution. <br>
Risk: Delete operations may be irreversible. <br>
Mitigation: Treat deletes as permanent and prefer listing or exporting affected records before deletion. <br>
Risk: Incorrect field value formats can cause failed writes or incorrect data. <br>
Mitigation: List field metadata before writing records and follow the documented per-field value formats for people, dates, select fields, URLs, and attachments. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/a3152557994-ship-it/feishu-bitable-suite) <br>
- [字段 Property 配置详解](references/field-properties.md) <br>
- [记录值数据结构详解](references/record-values.md) <br>
- [使用场景完整示例](references/examples.md) <br>
- [飞书开放平台字段编辑指南](https://go.feishu.cn/s/672BSzVyo03) <br>
- [飞书开放平台多维表格记录数据结构](https://go.feishu.cn/s/6lY28723w04) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, API calls, configuration, code] <br>
**Output Format:** [Markdown with JSON request examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces Feishu Bitable operation guidance, request shapes, field-format rules, and troubleshooting steps.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
