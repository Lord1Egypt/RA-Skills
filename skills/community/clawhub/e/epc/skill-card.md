## Description:

按品牌/车型/VIN 查 EPC 结构树、分解图与零件信息。当用户说：查一下这款大众的 EPC 爆炸图、这个零件在图里编号多少？或类似配件 EPC 问题时，使用本技能。

This skill is ready for commercial/non-commercial use.

## Publisher:

[jisuapi](https://clawhub.ai/user/jisuapi)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to query JisuAPI EPC data for vehicle model hierarchy, VIN lookup, EPC groups, exploded diagram structure, and parts information. It supports auto-parts workflows such as identifying a VIN's vehicle record, browsing EPC trees, and locating part numbers within grouped assemblies.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: EPC queries, including VIN values, are sent to JisuAPI.

Mitigation: Use the skill only when sending vehicle identifiers to JisuAPI is acceptable for the user's workflow and data handling requirements.

Risk: JISU_API_KEY is a paid API credential that may appear in logs or shell history if handled carelessly.

Mitigation: Store the key in the environment, rotate it if exposed, and avoid sharing logs, command histories, or request URLs that contain credentials or VINs.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jisuapi/skills/epc)
- [JisuAPI](https://www.jisuapi.com/)
- [JisuAPI Auto Parts EPC API](https://www.jisuapi.com/api/epc/)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown guidance with shell commands and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3 and JISU_API_KEY; API calls return JSON from JisuAPI.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
