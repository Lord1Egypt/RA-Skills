## Description: <br>
OpenClaw security patrol tool that runs one-click system security scans and generates easy-to-understand reports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[williamwang-wh](https://clawhub.ai/user/williamwang-wh) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
OpenClaw users and operators use this skill to run local or full security audits, optionally schedule daily patrols, and receive concise scan summaries that the agent can explain in plain language. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Full and scheduled audit modes can repeatedly send host-identifying audit metadata to a remote CTCT service. <br>
Mitigation: Prefer local-only mode on privacy-sensitive machines, and enable scheduled --push runs only after reviewing the disclosed data sharing. <br>
Risk: Scheduled patrols may continue running after initial setup. <br>
Mitigation: Review OpenClaw cron jobs after setup and use the documented OpenClaw cron commands to list, modify, or remove the scheduled audit. <br>


## Reference(s): <br>
- [OpenClaw Cron Setup Guide](references/cron-setup.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/williamwang-wh/claw-ctct-security-patrol) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown summaries, shell commands, and local text/JSON audit reports] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The audit script writes reports under ~/.openclaw/security-reports and the skill asks before providing detailed report interpretation.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
