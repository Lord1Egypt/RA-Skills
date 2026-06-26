## Description: <br>
Query Alibaba Cloud WAF block reasons via SLS logs and WAF CLI, analyze blocked requests, and optionally assist with tightly constrained WAF rule or log-service operations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sdk-team](https://clawhub.ai/user/sdk-team) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, cloud operators, and security engineers use this skill to investigate Alibaba Cloud WAF block pages by request ID, query WAF/SLS logs, identify triggering rules, and generate a concise block analysis report. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses Alibaba Cloud WAF and SLS credentials and can expose cloud operational data during troubleshooting. <br>
Mitigation: Install only for intended Alibaba Cloud WAF/SLS use, prefer least-privilege RAM roles, and limit log access to the projects and logstores needed for investigation. <br>
Risk: Some workflows can enable WAF logging or disable a WAF rule when remediation is requested. <br>
Mitigation: Require explicit user confirmation before write actions, query the current state first, grant modify permissions only when remediation is needed, and never delete rules or modify rule content. <br>
Risk: The documented CLI installation path includes piping a remote setup script to bash. <br>
Mitigation: Prefer a verified Aliyun CLI installation method and verify the installed CLI version before running WAF or SLS commands. <br>


## Reference(s): <br>
- [RAM Policy Requirements](references/ram-policies.md) <br>
- [Rule Configuration Details](references/rule-config-details.md) <br>
- [Rule Operation Policy](references/rule-operations.md) <br>
- [Common WAF Block Reasons](references/common-block-reasons.md) <br>
- [WAF OpenAPI](https://help.aliyun.com/zh/waf/web-application-firewall-3-0/developer-reference) <br>
- [ClawHub skill page](https://clawhub.ai/sdk-team/alibabacloud-waf-checkresponse-intercept-query) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/sdk-team) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown report with inline shell commands and configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Masks sensitive request details such as client IPs, query parameter values, cookies, authorization data, tokens, and long user-agent strings in reported log output.] <br>

## Skill Version(s): <br>
0.0.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
