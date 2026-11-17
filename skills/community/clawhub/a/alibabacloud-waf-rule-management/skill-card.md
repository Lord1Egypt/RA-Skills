## Description: <br>
Alibaba Cloud WAF 3.0 read-only diagnostic assistant for interception diagnosis, rule queries, and text-only configuration guidance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sdk-team](https://clawhub.ai/user/sdk-team) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and cloud operations engineers use this skill to diagnose Alibaba Cloud WAF interceptions, inspect existing WAF rules and SLS logs, and receive manual console guidance without automated configuration changes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses cloud credentials and can access Alibaba Cloud WAF configuration and SLS logs. <br>
Mitigation: Use a dedicated least-privilege RAM user or temporary credentials, do not paste secrets into chat, and confirm the active account and region before running commands. <br>
Risk: Diagnostic rule and log files may contain sensitive WAF, traffic, or account information. <br>
Mitigation: Treat saved diagnostic JSON as sensitive, keep it only as long as needed, and delete temporary files after the workflow. <br>
Risk: Read-only diagnostics can still query production cloud resources and produce misleading results if credentials, regions, or logstore names are wrong. <br>
Mitigation: Review each command before execution, use only documented read-only Describe/Get/SLS log queries, and verify the account, region, and User-Agent session value. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/sdk-team/skills/alibabacloud-waf-rule-management) <br>
- [WAF 3.0 OpenAPI Parameter Specification](references/api_reference.md) <br>
- [WAF CLI Command Reference](references/cli_commands.md) <br>
- [Alibaba Cloud CLI Operation Reference](references/cli_guide.md) <br>
- [WAF CLI Traps Checklist](references/cli_traps.md) <br>
- [WAF Configuration Guidance Details](references/configuration_guide.md) <br>
- [Alibaba Cloud CLI Profile Configuration Guide](references/profile_setup_guide.md) <br>
- [RAM Permission Statement](references/ram-policies.md) <br>
- [Security Rules - Complete Prohibitions](references/security_rules.md) <br>
- [WAF Skill Common Issues Troubleshooting](references/troubleshooting.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration guidance] <br>
**Output Format:** [Markdown with read-only shell commands and plain-language console guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs must remain text-only for configuration guidance and must not include executable write operations, generated scripts, or saved configuration files.] <br>

## Skill Version(s): <br>
0.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
