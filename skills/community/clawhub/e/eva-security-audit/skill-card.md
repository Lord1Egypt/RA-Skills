## Description: <br>
Runs a non-interactive OpenClaw security audit and produces a structured BLUF report with posture rating, ranked findings, and copy-paste fix commands. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[infectit007](https://clawhub.ai/user/infectit007) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, operators, and automation agents use this skill to run OpenClaw security audits, summarize posture quickly, and turn findings into prioritized remediation steps. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Security-audit findings may expose weaknesses if reports are stored locally or sent through Telegram. <br>
Mitigation: Use stdout-only unless persistent storage or Telegram delivery is intentional, and confirm the report contents before sharing. <br>
Risk: The security summary reports a mismatch between read-only/no-network safety claims and behavior that can store reports or send them through Telegram. <br>
Mitigation: Review delivery targets, bot token usage, chat destination, and cron schedule before installing or running scheduled audits. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/infectit007/eva-security-audit) <br>
- [Publisher profile](https://clawhub.ai/user/infectit007) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown BLUF report with ranked findings and copy-paste fix commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May print to stdout, append to local memory, or send through Telegram when intentionally configured.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
