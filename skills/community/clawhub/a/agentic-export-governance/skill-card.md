## Description: <br>
识别导出风险、应用脱敏规则、生成审批流程与审计记录。当用户需要导出研究结果或提交审批时触发。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[emergenceronearth](https://clawhub.ai/user/emergenceronearth) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Researchers, operators, and agent workflows use this skill to handle standalone result-export and approval tasks by reviewing export risk, desensitization rules, approval details, and audit records. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may display approval, audit, and patient-level risk details from local governance data. <br>
Mitigation: Use it only in the intended local export-governance workflow and review whether those details should be exposed to the agent or user. <br>
Risk: The skill reports status to `localhost:5001/api/report`. <br>
Mitigation: Confirm that the local report endpoint is expected before installation or execution. <br>
Risk: The skill depends on `/home/ubuntu/workspace/demo/mock_data/governance.json` for its governance content. <br>
Mitigation: Confirm that the local file exists and contains appropriate data for the intended environment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/emergenceronearth/agentic-export-governance) <br>
- [Publisher profile](https://clawhub.ai/user/emergenceronearth) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown response with governance summaries, tables, and local status-report shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reads a fixed local governance JSON file when present and reports status to a localhost endpoint.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
