## Description: <br>
PAI-EAS service diagnosis and troubleshooting for startup failures, error logs, slow responses, instance restarts, OOMKilled, ImagePullBackOff, CrashLoopBackOff, GPU errors, health check failures, liveness probe issues, and inaccessible services. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sdk-team](https://clawhub.ai/user/sdk-team) <br>

### License/Terms of Use: <br>
Apache-2.0 <br>


## Use Case: <br>
Alibaba Cloud PAI-EAS operators, SREs, and support engineers use this skill to diagnose running EAS service issues with read-only Aliyun CLI queries. It helps collect service status, events, logs, instance/container state, gateway/resource information, and diagnostic reports before producing troubleshooting guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can autonomously use an existing Alibaba Cloud profile to read PAI-EAS service inventory, logs, events, endpoints, and diagnostic data. <br>
Mitigation: Run it with a least-privilege read-only RAM role and avoid root accounts or long-lived access keys. <br>
Risk: Diagnostic output may include service tokens, AK/SK values, endpoints, or sensitive log content if shared without review. <br>
Mitigation: Redact credentials, service tokens, endpoints, and sensitive logs before sharing diagnosis output. <br>
Risk: Health-check disabling guidance can affect production availability if applied casually. <br>
Mitigation: Treat health-check disabling as non-production-only unless an operator explicitly approves the change and tracks rollback. <br>
Risk: The CLI and plugin setup is broad and may alter local Aliyun CLI behavior. <br>
Mitigation: Review CLI and plugin setup before execution and disable AI-Mode when diagnosis is complete. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/sdk-team/alibabacloud-pai-eas-service-diagnose) <br>
- [CLI Installation Guide](references/cli-installation-guide.md) <br>
- [Diagnosis Flow Guide](references/diagnosis-flow.md) <br>
- [Diagnostic API Quick Reference](references/api-reference.md) <br>
- [Related API List](references/related-apis.md) <br>
- [RAM Policies](references/ram-policies.md) <br>
- [Error Code Reference](references/error-codes.md) <br>
- [Health Check Configuration Reference](references/health-check.md) <br>
- [Verification Method](references/verification-method.md) <br>
- [Acceptance Criteria](references/acceptance-criteria.md) <br>
- [Aliyun CLI installer](https://aliyuncli.alicdn.com/install.sh) <br>
- [Alibaba Cloud RAM console](https://ram.console.aliyun.com/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown diagnosis report with inline Aliyun CLI commands and troubleshooting guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses an existing Alibaba Cloud CLI profile and should avoid printing access keys, service tokens, endpoints, or sensitive logs.] <br>

## Skill Version(s): <br>
0.0.1-beta.1 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
