## Description: <br>
ZeeLin Deep Research 深度研究是一款 AI 驱动的专业研究辅助平台，支持一句话生成与多步骤生成，提供深度、专家两大研究路径。从快速信息梳理、系统分析到超万字专家报告全流程覆盖，依托多轮推理与多源数据整合，高效完成企业分析、市场洞察、招商研究等复杂任务，一站式提升研究效率与决策质量。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhushanwei](https://clawhub.ai/user/zhushanwei) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and agents use this skill to submit research prompts to ZeeLin Deep Research, poll for completion, and retrieve generated reports for market, company, policy, technology, and business analysis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Research prompts and generated reports are sent to ZeeLin, and Feishu delivery can place report content into a Feishu document. <br>
Mitigation: Use the skill only when ZeeLin and the delivery platform are approved for the data being submitted; avoid secrets, regulated data, and confidential business material unless explicitly authorized. <br>
Risk: Generated reports may be downloaded to temporary local files before being sent to the user. <br>
Mitigation: Delete temporary report files after delivery when handling sensitive content. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zhushanwei/desearch) <br>
- [Publisher profile](https://clawhub.ai/user/zhushanwei) <br>
- [ZeeLin Deep Research service](https://desearch.zeelin.cn) <br>
- [ZeeLin API key and credits page](https://desearch.zeelin.cn/skill-activity) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, Files] <br>
**Output Format:** [Markdown guidance with bash and JSON examples; generated research reports are retrieved as PDF or Word files and may be delivered as files or Feishu document links.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires curl and DESEARCH_API_KEY; report workflows may create temporary local files before delivery.] <br>

## Skill Version(s): <br>
1.0.12 (source: server release metadata and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
