## Description: <br>
Provides OpenClaw monitoring helpers for checking local system resources, gateway status, and scheduled cron jobs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[miaoxingjun](https://clawhub.ai/user/miaoxingjun) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators using OpenClaw use this skill to inspect local health and cron status for automated workflows. Advertised alerting and sub-agent tracking should be treated as limited unless additional implementation is supplied and reviewed. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The supplied scripts can display local OpenClaw cron and gateway status in the conversation. <br>
Mitigation: Install only where sharing that local status with the agent is acceptable. <br>
Risk: The scripts rely on the openclaw command found on PATH. <br>
Mitigation: Verify that the local openclaw binary is trusted before running the health or cron helpers. <br>
Risk: Feishu/chat push alerts and sub-agent tracking are advertised but not implemented in the supplied code. <br>
Mitigation: Treat those capabilities as unavailable until additional code is supplied and reviewed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/miaoxingjun/asclaude-monitor) <br>
- [README.md](artifact/README.md) <br>
- [SKILL.md](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown with inline shell commands and concise status summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May call local OpenClaw commands when the supplied helper scripts are run.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
