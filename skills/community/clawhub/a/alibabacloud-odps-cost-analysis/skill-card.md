## Description: <br>
Analyzes Alibaba Cloud MaxCompute (ODPS) pay-as-you-go costs across billing, storage, compute usage, and SQL signature metrics using approved Aliyun CLI MaxCompute APIs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sdk-team](https://clawhub.ai/user/sdk-team) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, cloud engineers, and FinOps teams use this skill to inspect Alibaba Cloud MaxCompute costs, trends, storage metrics, compute metrics, and SQL signature usage while staying within the documented MaxCompute CLI API set. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide an agent to run Aliyun CLI queries against an Alibaba Cloud account using sensitive credentials. <br>
Mitigation: Use a dedicated least-privilege RAM user or role, avoid long-lived secrets in command lines, and confirm the active CLI profile and region before running commands. <br>
Risk: The workflow depends on installing or updating the Aliyun CLI and MaxCompute plugin. <br>
Mitigation: Prefer trusted package-manager installation where possible, verify installer scripts before execution, and keep the MaxCompute plugin current. <br>
Risk: Using the wrong Alibaba Cloud product API could return misleading or overbroad billing information. <br>
Mitigation: Run only the documented `aliyun maxcompute` commands with the required user agent and do not substitute `bssopenapi` or other product APIs. <br>


## Reference(s): <br>
- [Related APIs](references/related-apis.md) <br>
- [RAM Policies](references/ram-policies.md) <br>
- [Aliyun CLI Installation & Configuration Guide](references/cli-installation-guide.md) <br>


## Skill Output: <br>
**Output Type(s):** [analysis, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline bash commands and cost-analysis summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses scoped Aliyun CLI MaxCompute commands and user-provided region and time range inputs.] <br>

## Skill Version(s): <br>
0.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
