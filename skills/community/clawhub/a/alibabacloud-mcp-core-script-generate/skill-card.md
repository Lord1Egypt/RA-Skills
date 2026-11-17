## Description: <br>
Generate Alibaba Cloud MCP Core RunScript-compatible Python scripts from natural-language cloud operation requests. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sdk-team](https://clawhub.ai/user/sdk-team) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and cloud operators use this skill to turn natural-language Alibaba Cloud operation requests into RunScript-compatible Python scripts that use the injected call_cli API and pass sandbox validation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated scripts can create, update, or delete Alibaba Cloud resources when the user requests write operations. <br>
Mitigation: Review generated scripts before running them and rely on the RunScript runtime approval flow for write operations. <br>
Risk: API metadata lookup can disclose the intended Alibaba Cloud product and action usage. <br>
Mitigation: Install and use the skill only when that level of metadata disclosure is acceptable. <br>
Risk: Incorrect API parameters or disallowed script patterns can produce scripts that fail sandbox validation or behave unexpectedly. <br>
Mitigation: Use the bundled sandbox checker and review any validation warnings before execution. <br>


## Reference(s): <br>
- [RunScript Contract Reference](references/runscript-contract.md) <br>
- [Alibaba Cloud API Docs Metadata](https://next.api.aliyun.com/meta/v1/products/{product}/versions/{version}/api-docs.json) <br>
- [Alibaba Cloud API Definition Metadata](https://api.aliyun.com/meta/v1/products/{product}/versions/{version}/apis/{action}/api.json) <br>
- [ClawHub Skill Page](https://clawhub.ai/sdk-team/skills/alibabacloud-mcp-core-script-generate) <br>


## Skill Output: <br>
**Output Type(s):** [code, shell commands, guidance] <br>
**Output Format:** [Python script body] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs only the generated script body by default; scripts assign final data to result and are validated before output.] <br>

## Skill Version(s): <br>
0.0.1 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
