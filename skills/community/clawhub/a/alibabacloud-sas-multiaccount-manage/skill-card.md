## Description: <br>
Manage multiple Alibaba Cloud accounts and batch-export Security Center (SAS) baseline and vulnerability reports via the aliyun CLI and Python scripts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sdk-team](https://clawhub.ai/user/sdk-team) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, cloud security engineers, and operations teams use this skill to manage Alibaba Cloud SAS multi-account participation and export baseline or vulnerability compliance reports across enabled accounts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses Alibaba Cloud credentials to run SAS export workflows across multiple accounts. <br>
Mitigation: Use least-privilege RAM credentials and review the included RAM policy guidance before running batch exports. <br>
Risk: Batch exports depend on the local account selection stored in accounts.json. <br>
Mitigation: Run account refresh intentionally and review accounts.json before enabling broad exports. <br>
Risk: The aliyun CLI AI-mode and User-Agent configuration can persist after setup. <br>
Mitigation: Check the CLI configuration after use and disable AI mode if it is no longer needed. <br>
Risk: Exported Security Center reports may contain sensitive security and account information. <br>
Mitigation: Run scripts in a dedicated working directory and handle generated JSON and Excel files according to internal data handling rules. <br>


## Reference(s): <br>
- [RAM Permission Policy Notes](references/ram-policies.md) <br>
- [Alibaba Cloud Security Center RAM Authorization](https://www.alibabacloud.com/help/en/security-center/developer-reference/api-sas-2018-12-03-ram) <br>
- [STS GetCallerIdentity](https://www.alibabacloud.com/help/en/resource-access-management/latest/getcalleridentity) <br>
- [Alibaba Cloud RAM Custom Policies](https://help.aliyun.com/zh/ram/user-guide/create-a-custom-policy) <br>
- [Alibaba Cloud CLI Releases](https://github.com/aliyun/aliyun-cli/releases) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration instructions, Files] <br>
**Output Format:** [Markdown with inline bash commands; scripts can produce JSON account lists and merged Excel reports] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires aliyun CLI credentials and a Python environment; generated files are written to the agent's current working directory.] <br>

## Skill Version(s): <br>
0.0.1 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
