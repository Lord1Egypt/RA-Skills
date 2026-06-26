## Description: <br>
Automatically update Clawdbot and all installed skills once daily. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xiyuechuimeng](https://clawhub.ai/user/xiyuechuimeng) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agent users and developers use this skill to set up scheduled daily updates for Clawdbot and installed skills, then receive a concise report of what changed. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Unattended daily updates can change Clawdbot and installed skills without per-update approval. <br>
Mitigation: Use dry-run or manual updates before enabling the schedule, review update summaries, and keep the documented cron removal command available. <br>


## Reference(s): <br>
- [Agent Implementation Guide](references/agent-guide.md) <br>
- [Update Summary Examples](references/summary-examples.md) <br>
- [Clawdbot Updating Guide](https://docs.clawd.bot/install/updating) <br>
- [ClawdHub CLI](https://docs.clawd.bot/tools/clawdhub) <br>
- [Cron Jobs](https://docs.clawd.bot/cron) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration] <br>
**Output Format:** [Markdown with shell commands and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes cron setup, update commands, troubleshooting guidance, and summary-message examples.] <br>

## Skill Version(s): <br>
1.0.0 (source: server evidence and skill metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
