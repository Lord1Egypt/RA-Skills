## Description: <br>
easy-openclaw guides users through OpenClaw setup and optimization, including base configuration, channel-specific Discord, Feishu, and Telegram tuning, optional skill installation, and new channel onboarding. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[daheiai](https://clawhub.ai/user/daheiai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
OpenClaw users and operators use this skill to collect configuration choices, apply confirmed OpenClaw settings, install selected supporting skills, and validate messaging channels without manually editing configuration files. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can modify OpenClaw configuration, create backups or Cron jobs, install components, and restart the gateway. <br>
Mitigation: Require a dry run before execution that lists file diffs, commands, backup location, new scheduled jobs, restart timing, and rollback steps. <br>
Risk: The skill may handle Discord, Telegram, or Feishu credentials while onboarding channels. <br>
Mitigation: Provide credentials only through an appropriate private channel, require redaction in logs and summaries, and rotate any credential exposed in a public or shared conversation. <br>
Risk: Broad exec permissions or allowlists can allow sensitive commands to run without the intended approval step. <br>
Mitigation: Review `tools.profile`, `tools.exec`, and `exec-approvals.json` before enabling execution, avoid broad allowlists on important systems, and test approvals with a controlled temporary file. <br>
Risk: Optional skill installation can add third-party dependencies or behavior beyond the base OpenClaw configuration workflow. <br>
Mitigation: Install only explicitly selected skills, verify upstream installation steps, and run the artifact's documented minimal validation before treating installation as complete. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/daheiai/easy-openclaw) <br>
- [README](README.md) <br>
- [Configuration overview](references/configs.md) <br>
- [Execution, restart, and closeout](references/execution.md) <br>
- [Troubleshooting and validation](references/troubleshooting.md) <br>
- [OpenClaw](https://github.com/openclaw-ai/openclaw) <br>
- [OpenClaw Backup](https://clawhub.ai/alex3alex/openclaw-backup) <br>
- [Agent Reach](https://github.com/Panniantong/Agent-Reach) <br>
- [OpenClaw security practice guide](https://github.com/slowmist/openclaw-security-practice-guide) <br>
- [Find Skills](https://clawhub.ai/JimLiuxinghai/find-skills) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown text with command snippets, configuration summaries, and validation results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May request credentials and user approval before applying persistent OpenClaw configuration changes.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
