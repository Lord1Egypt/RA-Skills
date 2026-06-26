## Description: <br>
Alibaba Cloud Tair (Redis OSS-Compatible) Database AI Assistant for Tair/Redis instance management, performance diagnostics, memory analysis, hotspot key detection, latency troubleshooting, parameter tuning, and connection session analysis. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sdk-team](https://clawhub.ai/user/sdk-team) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, database engineers, and operators use this skill to inspect Alibaba Cloud Tair or Redis-compatible instances, diagnose performance and memory issues, review backups and security configuration, and generate CLI-driven diagnostic workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses aliyun credentials and sends diagnostic prompts to Alibaba Cloud services. <br>
Mitigation: Use a dedicated low-privilege RAM profile, avoid secrets or customer data in prompts, and confirm the intended profile before invocation. <br>
Risk: CLI settings such as AI-Mode and automatic plugin installation can persist beyond a session. <br>
Mitigation: Review installer and configuration commands before use, then disable AI-Mode or revert persistent CLI settings after the workflow when they are no longer needed. <br>
Risk: Diagnostics can expose instance IDs, configuration details, and operational data. <br>
Mitigation: Confirm user-customizable parameters before commands and limit RAM permissions to read-only Tair plus YaoChi or DAS agent actions where possible. <br>


## Reference(s): <br>
- [CLI Installation Guide](references/cli-installation-guide.md) <br>
- [RAM Policies](references/ram-policies.md) <br>
- [Related APIs](references/related-apis.md) <br>
- [Verification Method](references/verification-method.md) <br>
- [Acceptance Criteria](references/acceptance-criteria.md) <br>
- [Alibaba Cloud RAM permission guide](https://help.aliyun.com/document_detail/116146.html) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown and terminal text with bash command examples and streamed diagnostic response text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include session IDs on stderr for multi-turn diagnostics; requires aliyun CLI, DAS plugin, jq, and configured Alibaba Cloud credentials.] <br>

## Skill Version(s): <br>
0.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
