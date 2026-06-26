## Description: <br>
Perform security inspection and monitoring for Alibaba Cloud DDoS security products, covering DDoS Basic Protection, DDoS Native Protection, and DDoS Anti-DDoS Pro/Premium. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sdk-team](https://clawhub.ai/user/sdk-team) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Cloud security operators, developers, and engineers use this skill to inspect Alibaba Cloud DDoS product coverage, query attack and traffic events, verify product-specific API routing, and produce a DDoS security inspection report. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can use the local Aliyun CLI profile to query broad Alibaba Cloud DDoS security and asset data. <br>
Mitigation: Install and run it only for intended DDoS inspection work, and prefer a dedicated least-privilege RAM account with the documented read-only permissions. <br>
Risk: The skill can run CLI setup commands, update plugins, and change local AI-mode settings. <br>
Mitigation: Review the exact setup steps before execution, verify the Aliyun CLI installer source before using the pipe-to-bash installer, and confirm CLI plugin and AI-mode state after the workflow exits. <br>
Risk: Incorrect region or product selection could produce misleading inspection results. <br>
Mitigation: Confirm products, regions, and time windows before execution, and follow the skill's product-isolation and endpoint-routing checks. <br>


## Reference(s): <br>
- [CLI Installation Guide](references/cli-installation-guide.md) <br>
- [CLI Credential Setup](references/cli-setup.md) <br>
- [RAM Permission Policies](references/ram-policies.md) <br>
- [API Parameter Reference](references/api-reference.md) <br>
- [CLI Command Table](references/related-commands.md) <br>
- [Inspection Report Template](references/report-template.md) <br>
- [Verification Method](references/verification-method.md) <br>
- [Acceptance Criteria](references/acceptance-criteria.md) <br>
- [Alibaba Cloud CLI Official Docs](https://help.aliyun.com/zh/cli/) <br>
- [Alibaba Cloud CLI RPC and ROA API Calls](https://help.aliyun.com/zh/cli/call-rpc-api-and-roa-api) <br>
- [Aliyun CLI Releases](https://github.com/aliyun/aliyun-cli/releases) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown report and inline shell commands using Aliyun CLI OpenAPI calls] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include command output summaries, region-by-region asset inventories, anomaly findings, and verification notes.] <br>

## Skill Version(s): <br>
0.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
