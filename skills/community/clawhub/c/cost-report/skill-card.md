## Description: <br>
Track OpenClaw usage costs and provide detailed reports by date and model. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[vincentqiu](https://clawhub.ai/user/vincentqiu) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and engineers use this skill to inspect OpenClaw session logs, summarize model usage costs by date and model, and prepare daily, weekly, monthly, or custom cost reports for operational review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The release security summary reports unsafe command execution when untrusted CLI arguments are passed through the Node wrapper. <br>
Mitigation: Use the shell script directly with documented flags or review and harden the wrapper before accepting untrusted arguments. <br>
Risk: Discord-oriented reports and the --show-errors path can expose session-log error details that may contain sensitive content. <br>
Mitigation: Avoid report_discord.sh and --show-errors when session errors may contain confidential data, and review report output before sharing it to messaging channels. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/vincentqiu/cost-report) <br>
- [JSONL_FORMAT.md](references/JSONL_FORMAT.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Plain text, JSON, Discord-oriented Markdown, and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports may include date ranges, model-level cost breakdowns, percentage changes, and cron configuration examples.] <br>

## Skill Version(s): <br>
1.0.2 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
