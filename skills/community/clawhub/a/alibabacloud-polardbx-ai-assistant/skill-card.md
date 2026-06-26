## Description: <br>
Alibaba Cloud PolarDB-X Distributed Database AI Assistant for cluster management, topology inspection, performance diagnostics, SQL optimization, data distribution analysis, scaling diagnostics, session analysis, security audit, backup and restore checks, parameter tuning, and other operations tasks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sdk-team](https://clawhub.ai/user/sdk-team) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers, DBAs, and cloud operations teams use this skill to run Alibaba Cloud PolarDB-X diagnostics through the Aliyun CLI DAS YaoChi Agent workflow. It helps inspect cluster topology, performance, slow SQL, sessions, backups, security posture, data distribution, and related operational status. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses an Aliyun CLI profile that may have access to sensitive Alibaba Cloud resources. <br>
Mitigation: Use a profile intended for PolarDB-X diagnostics, preferably OAuth, STS, or a least-privilege RAM role. <br>
Risk: Access keys, tokens, or production database details could be exposed if pasted into chat or logged commands. <br>
Mitigation: Do not paste real access keys into chat or shell commands, and avoid sending secrets or highly sensitive production details in diagnostic prompts. <br>
Risk: The setup flow references remote installer and plugin update commands. <br>
Mitigation: Review any remote installer before executing it and update or install CLI plugins from trusted sources. <br>
Risk: AI-mode is enabled for skill execution and could remain active after the diagnostic task. <br>
Mitigation: Disable AI-mode at every exit point after completing, failing, or cancelling the workflow. <br>
Risk: The underlying service can throttle concurrent diagnostic sessions. <br>
Mitigation: Avoid more than two concurrent sessions per account and wait or retry when throttling is reported. <br>


## Reference(s): <br>
- [Aliyun CLI Installation & Configuration Guide](references/cli-installation-guide.md) <br>
- [Related APIs](references/related-apis.md) <br>
- [RAM Policies](references/ram-policies.md) <br>
- [Verification Method](references/verification-method.md) <br>
- [Acceptance Criteria](references/acceptance-criteria.md) <br>
- [Aliyun CLI Official Documentation](https://help.aliyun.com/zh/cli/) <br>
- [Aliyun CLI Plugin Repository](https://github.com/aliyun/aliyun-cli) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell command examples and streamed text responses from Alibaba Cloud DAS/YaoChi.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses an existing Aliyun CLI credential profile and may return a session ID for multi-turn diagnostics.] <br>

## Skill Version(s): <br>
0.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
