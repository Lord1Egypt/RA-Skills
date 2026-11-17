## Description: <br>
Alibaba Cloud SRE skill for cloud infrastructure diagnosis, health inspection, capacity planning, incident response, and security audit, with STAROps workflows and controlled CLI fallback for read-only diagnosis. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sdk-team](https://clawhub.ai/user/sdk-team) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and SRE teams use this skill to diagnose Alibaba Cloud ECS, ACK, pod, resource utilization, incident, capacity, architecture, and security-audit issues. It guides agents through STAROps-first workflows, controlled read-only CLI fallback, and actionable Markdown reports with remediation recommendations for manual execution. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide STAROps onboarding actions that include high-impact delete operations. <br>
Mitigation: Require explicit human approval for delete-employee or account-delete actions and avoid granting routine diagnostic credentials DeleteDigitalEmployee permission. <br>
Risk: The skill requires access to Alibaba Cloud profiles and STAROps administration. <br>
Mitigation: Use least-privilege RAM permissions and separate routine diagnostic credentials from onboarding or administrative credentials. <br>
Risk: Local execution traces may persist diagnostic prompts or sensitive operational context. <br>
Mitigation: Review .aliyun-sre/execution-trace.jsonl for sensitive content and redact credentials, tokens, and secrets before sharing outputs. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/sdk-team/skills/alibabacloud-sre-toolkit) <br>
- [RAM Policies](references/ram-policies.md) <br>
- [Initialization Guide](references/initialization-guide.md) <br>
- [Session Management](references/session-management.md) <br>
- [STAROps API](references/starops-api.md) <br>
- [CLI Installation Guide](references/cli-installation-guide.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown reports and guidance with inline shell commands and local JSONL execution traces] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Diagnostic workflows are intended to be read-only; remediation is presented as manual user-executed guidance.] <br>

## Skill Version(s): <br>
0.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
