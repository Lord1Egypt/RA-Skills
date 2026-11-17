## Description:

ZeeLin Deep Research 深度研究是一款 AI 驱动的专业研究辅助平台，支持一句话生成与多步骤生成，提供深度、专家两大研究路径。从快速信息梳理、系统分析到超万字专家报告全流程覆盖，依托多轮推理与多源数据整合，高效完成企业分析、市场洞察、招商研究等复杂任务，一站式提升研究效率与决策质量。

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhushanwei](https://clawhub.ai/user/zhushanwei)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to submit research prompts to ZeeLin Deep Research, choose a deep or major research mode, poll task status, and deliver generated research reports. Typical tasks include market research, company analysis, policy review, technical comparison, and investment or business decision support.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Research prompts and generated reports are sent to the external ZeeLin service and may also be forwarded through a messaging or Feishu channel.

Mitigation: Use only content approved for those transfers, avoid confidential or regulated material unless the organization permits it, and confirm the destination channel before delivery.

Risk: The workflow downloads report files from returned URLs and sends local files automatically.

Mitigation: Validate the returned report URL and downloaded file before sending, use per-run private temporary directories, and delete temporary files after delivery.

Risk: The security scan marked the skill suspicious because automated sharing instructions have weak safeguards.

Mitigation: Review before installing and require human confirmation for recipients, channels, and report contents before distribution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zhushanwei/skills/desearch)
- [ClawHub publisher profile](https://clawhub.ai/user/zhushanwei)
- [ZeeLin Deep Research service](https://desearch.zeelin.cn)
- [ZeeLin API key and credits page](https://desearch.zeelin.cn/skill-activity)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON API responses, bash command examples, and downloaded PDF or document report files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires curl and a DESEARCH_API_KEY; report delivery may use local temporary files or a messaging/document channel.]

## Skill Version(s):

1.0.12 (source: server-resolved release metadata and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
