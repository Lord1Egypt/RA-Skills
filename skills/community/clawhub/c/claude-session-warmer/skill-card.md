## Description: <br>
Claude Session Warmer helps users align Claude Pro/Max usage windows to working hours by scheduling small official Claude Code CLI primer prompts on an always-on box. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[daryn-louw](https://clawhub.ai/user/daryn-louw) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators who run Claude Code on an always-on VPS use this skill to generate setup guidance, cron commands, and configuration for scheduled primer prompts that align Claude usage windows with their workday. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Unattended scheduled Claude CLI prompts can consume account quota and depend on current Claude or Anthropic subscription policy. <br>
Mitigation: Install only when intentional, keep enabled=false until ready, use a trivial primer prompt, and verify current Claude or Anthropic terms before enabling the schedule. <br>
Risk: The skill requires an authenticated Claude Code CLI on an always-on VPS and handles a sensitive account context. <br>
Mitigation: Log in on the VPS through the official Claude flow and avoid copying OAuth tokens or credentials between machines. <br>
Risk: The install flow prints cron entries that can run prompts repeatedly if added without review. <br>
Mitigation: Review the generated cron block before adding it and use the documented check, schedule, dry_run, and enabled controls before unattended use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/daryn-louw/claude-session-warmer) <br>
- [Project website](https://decisionvex.github.io/claude-session-warmer/) <br>
- [Terms and usage boundaries](references/tos.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces guidance for Node-based checks, schedule previews, cron installation, and config.json setup; it does not generate authentication tokens.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
