## Description: <br>
Diagnoses Alibaba Cloud PAI-EAS service health issues such as startup failures, error logs, restarts, OOMKilled, GPU errors, liveness probe failures, and inaccessible services. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sdk-team](https://clawhub.ai/user/sdk-team) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and cloud operations engineers use this skill to run read-only PAI-EAS diagnostics, inspect service status, events, logs, instances, containers, and diagnosis reports, and produce health analysis with recommendations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can give an agent broad read access to PAI-EAS service metadata, events, logs, endpoints, and service tokens. <br>
Mitigation: Use a least-privilege read-only RAM role and install only when this diagnostic access is appropriate for the environment. <br>
Risk: Account-wide discovery or vague service selection can expose more cloud service information than needed. <br>
Mitigation: Specify the exact region and service before running diagnostics and avoid account-wide discovery unless it is necessary. <br>
Risk: Diagnostic output may include sensitive tokens, authorization headers, access keys, logs, or endpoint details. <br>
Mitigation: Redact credentials, tokens, headers, logs, and endpoint details before sharing diagnostic output. <br>


## Reference(s): <br>
- [Skill page](https://clawhub.ai/sdk-team/skills/alibabacloud-pai-eas-service-diagnose) <br>
- [CLI Installation Guide](references/cli-installation-guide.md) <br>
- [Diagnostic API Quick Reference](references/api-reference.md) <br>
- [Diagnosis Flow Guide](references/diagnosis-flow.md) <br>
- [Error Code Reference](references/error-codes.md) <br>
- [Health Check Configuration Reference](references/health-check.md) <br>
- [RAM Policies](references/ram-policies.md) <br>
- [Related API List](references/related-apis.md) <br>
- [Verification Method](references/verification-method.md) <br>
- [Acceptance Criteria](references/acceptance-criteria.md) <br>
- [Aliyun CLI downloads](https://aliyuncli.alicdn.com/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown diagnosis report with inline shell commands and summarized CLI output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Aliyun CLI and jq; uses read-only PAI-EAS APIs and a per-session user-agent.] <br>

## Skill Version(s): <br>
0.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
