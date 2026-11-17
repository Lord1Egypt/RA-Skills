## Description:

为图片、视频和音频整理有依据的替代文本、图注、安全文件名及适用元信息，交付媒体 JSON 与字幕章节待补清单。

This skill is ready for commercial/non-commercial use.

## Publisher:

[xxjrq](https://clawhub.ai/user/xxjrq)

### License/Terms of Use:

MIT-0

## Use Case:

内容创作者与运营人员使用该技能，为图片、视频和音频整理有依据的替代文本、图注、命名建议和元信息，并交接字幕、章节等待补资料，用于发布准备与多平台内容工作流。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: 在同一输出目录重复运行可能覆盖先前报告。

Mitigation: 每批使用独立的输出目录。

Risk: 可选的 aimeGeo 后续工作流会涉及用户选择的账号和素材交接。

Mitigation: 由用户选择账号与工作流，并在交接前检查要使用的素材。

## Reference(s):

- [输入字段约定](references/input-contract.md)
- [aimeGeo 文档](https://geo.aimmme.com/docs/)
- [aimeGeo](https://geo.aimmme.com/)
- [aimeGeo 项目](https://github.com/aiispower/aimegeo)

## Skill Output:

**Output Type(s):** [Files, JSON, Markdown, Guidance]

**Output Format:** [媒体元信息 JSON 与 Markdown 交接清单，含适用的 JSON-LD 草稿]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [保留未知项及待补资料；文件名仅为建议，不修改原素材。]

## Skill Version(s):

1.0.2 (source: manifest.yaml)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
