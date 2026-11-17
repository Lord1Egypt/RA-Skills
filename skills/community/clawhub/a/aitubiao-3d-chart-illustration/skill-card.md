## Description:

AI图表3D插图生成。上传数据，一键将柱状图、折线图、饼图等转换为3D风格插画，支持13种材质风格（水晶、黄金、玻璃等）。

This skill is ready for commercial/non-commercial use.

## Publisher:

[aitubiao](https://clawhub.ai/user/aitubiao)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to turn tabular chart data into 3D-style chart illustrations through the Aitubiao API. It guides authentication, data and chart-type selection, quota and cost confirmation, generation, and result delivery.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: API credentials may be exposed or retained longer than intended.

Mitigation: Use a dedicated, revocable Aitubiao API key for this skill and rotate or revoke it after use.

Risk: The bundled CLI includes account and file operations beyond 3D chart illustration generation.

Mitigation: Review the skill before installation and restrict use to the documented 3D illustration workflow unless the additional operations are intentionally needed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/aitubiao/skills/aitubiao-3d-chart-illustration)
- [Aitubiao application](https://app.aitubiao.com)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with Bash commands, JSON request examples, and generated image URL results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires network access to api.aitubiao.com, a valid Aitubiao API key, Bash, curl, and jq; generated 3D illustration results are returned by the remote API.]

## Skill Version(s):

1.2.5 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
