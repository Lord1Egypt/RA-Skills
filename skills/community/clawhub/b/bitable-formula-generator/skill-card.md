## Description:

飞书多维表格字段公式生成器。通过导出Excel分析字段结构，利用Excel公式逻辑生成多维表格兼容公式，并写入多维表格字段。

This skill is ready for commercial/non-commercial use.

## Publisher:

[chengfen1987](https://clawhub.ai/user/chengfen1987)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to inspect Feishu Bitable table structure, generate formulas from Excel-style logic, and optionally create or update Feishu formula fields.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can use Feishu app credentials to inspect table schemas and create or update formula fields.

Mitigation: Use a least-privileged Feishu app and provide credentials only through the documented environment variables.

Risk: Generated formulas or API write operations could change production Bitable fields incorrectly.

Mitigation: Review set-formula or direct PUT/POST operations before execution and test formula changes on a duplicate table when possible.

## Reference(s):

- [Bitable function and Excel function reference](references/api_reference.md)
- [Feishu Bitable field API endpoint](https://open.feishu.cn/open-apis/bitable/v1/apps/{app_token}/tables/{table_id}/fields/{field_id})
- [ClawHub skill page](https://clawhub.ai/chengfen1987/skills/bitable-formula-generator)
- [Publisher profile](https://clawhub.ai/user/chengfen1987)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown with formulas, command examples, and API request guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include Feishu Bitable formulas, Node.js command invocations, and field update instructions.]

## Skill Version(s):

1.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
