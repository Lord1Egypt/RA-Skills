## Description: <br>
Calculate Claude Max subscription usage from OpenClaw session data, including credits consumed, weekly budget percentage, 5-hour rate-limit window, and per-session breakdown. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lemodigital](https://clawhub.ai/user/lemodigital) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
OpenClaw users and developers use this skill to estimate Claude Max subscription consumption from local OpenClaw session transcripts, review remaining weekly budget, and inspect high-usage sessions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The tool reads local OpenClaw session logs, which may contain private conversation content. <br>
Mitigation: Install and run it only in environments where reading those local logs is acceptable. <br>
Risk: Using --save stores reset time, plan, and timezone locally. <br>
Mitigation: Use --save only when persistent local configuration is desired. <br>


## Reference(s): <br>
- [Claude Usage ClawHub page](https://clawhub.ai/lemodigital/claude-usage) <br>
- [OpenClaw](https://openclaw.ai) <br>
- [Claude Max limits reference](https://she-llac.com/claude-limits) <br>
- [Claude](https://claude.ai) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, text, JSON] <br>
**Output Format:** [Terminal text reports or JSON, with setup guidance and shell commands in Markdown] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May read local OpenClaw session logs and may save reset time, plan, and timezone to a local OpenClaw configuration file when requested.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
