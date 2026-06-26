## Description: <br>
将需求文档、表单字段规则、审批流程定义和 UI 说明转化为结构化测试用例，适用于表单校验、流程审批、状态流转、权限隔离和业务分支测试场景。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Lens-lzy](https://clawhub.ai/user/Lens-lzy) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
QA testers, product managers, and developers use this skill to turn PRDs, field rules, approval workflows, UI notes, and screenshot descriptions into executable test cases and requirement-confirmation questions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: PRDs, approval workflows, and generated test cases may contain sensitive business details when exported to Feishu, cloud drive, or local files. <br>
Mitigation: Use in-chat Markdown output by default, and request Feishu, cloud-drive, or local-file export only for approved destinations. <br>
Risk: Generated test cases may expose ambiguities or gaps in incomplete requirements rather than resolving the underlying business decision. <br>
Mitigation: Review the requirement-confirmation questions and resolve open points before using the test cases for execution or signoff. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Lens-lzy/easy-testcase) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance, Files] <br>
**Output Format:** [Markdown table with optional requirement-confirmation table] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create Feishu, cloud-drive, or local-file outputs only when requested and when the required tools are available.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
