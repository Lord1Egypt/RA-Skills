## Description: <br>
Monitor OpenClaw Gateway health by detecting abnormal error rates in logs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[guoqunabc](https://clawhub.ai/user/guoqunabc) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill to monitor OpenClaw Gateway logs, detect abnormal error rates, and surface rate limiting, server, authentication, network, and delivery failures before they exhaust quotas or disrupt message delivery. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads OpenClaw and systemd logs and writes local monitoring state and history. <br>
Mitigation: Install only when local Gateway log monitoring is desired, and review alert output before forwarding it. <br>
Risk: Untrusted custom patterns could alter log matching behavior. <br>
Mitigation: Avoid untrusted WATCHDOG_EXTRA_PATTERNS values and keep custom patterns scoped to expected Gateway errors. <br>
Risk: Optional cron or heartbeat integration can create recurring checks. <br>
Mitigation: Enable recurring execution only when continuous monitoring is intended. <br>


## Reference(s): <br>
- [Gateway Watchdog on ClawHub](https://clawhub.ai/guoqunabc/gateway-watchdog) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline bash commands and terminal output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write local state and history under the configured user state directory.] <br>

## Skill Version(s): <br>
1.4.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
