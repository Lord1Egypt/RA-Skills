## Description: <br>
PAI-DLC job diagnostics and health inspection for queuing-stuck root cause analysis, failed-job localization, and cluster health checks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sdk-team](https://clawhub.ai/user/sdk-team) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and ML platform engineers use this skill to investigate Alibaba Cloud PAI-DLC jobs that are queuing, failed, running, or completed by collecting read-only job state, events, logs, sanity-check results, and resource-diagnosis signals. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires Alibaba Cloud credentials and can expose cloud account access if credentials are overprivileged or pasted into an agent session. <br>
Mitigation: Use a dedicated least-privilege RAM user or temporary credentials, configure credentials outside the agent session, and never paste raw AK/SK values. <br>
Risk: Diagnostic outputs can include job metadata, pod logs, events, or console links that reveal operational details. <br>
Mitigation: Redact job metadata and pod logs before sharing reports outside the intended audience. <br>
Risk: Persistent Aliyun CLI settings can remain after the diagnostic session. <br>
Mitigation: Review Aliyun CLI settings after use and disable AI mode when the session ends. <br>


## Reference(s): <br>
- [Acceptance Criteria](references/acceptance-criteria.md) <br>
- [Aliyun CLI Installation & Configuration Guide](references/cli-installation-guide.md) <br>
- [Failure Pattern Knowledge Base](references/diagnostic-patterns.md) <br>
- [Health-Inspection Dimensions and Interpretation Rules](references/healthcheck-dimensions.md) <br>
- [RAM Permissions](references/ram-policies.md) <br>
- [Related CLI Commands](references/related-commands.md) <br>
- [PAI Studio Resource Diagnosis API](references/resource-diagnosis-api.md) <br>
- [Verification Method](references/verification-method.md) <br>
- [Aliyun CLI Official Documentation](https://help.aliyun.com/zh/cli/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown diagnostic reports with inline shell commands and console links] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Read-only diagnostics; API command output should be capped with max-lines and max-events limits where the skill specifies them.] <br>

## Skill Version(s): <br>
0.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
