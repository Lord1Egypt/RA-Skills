## Description: <br>
Claw News generates daily news digests from user-managed topics, AI/search APIs, RSS feeds, and site-specific trackers, with optional scheduled delivery. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[russellfei](https://clawhub.ai/user/russellfei) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill to configure an agent that tracks chosen news topics, RSS categories, and Kickstarter projects, then produces concise daily digests. It is intended for recurring personal or team news monitoring with optional Slack or channel delivery. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security scan reports embedded live-looking API keys. <br>
Mitigation: Review the code before installing, remove embedded keys, and rotate any exposed credentials before use. <br>
Risk: The skill can send search topics, RSS content, and generated summaries to external AI and search providers. <br>
Mitigation: Use only providers approved for the data being processed and avoid submitting sensitive topics or private content. <br>
Risk: Cron and Slack delivery examples can create scheduled background runs and message posting. <br>
Mitigation: Enable scheduled jobs or channel delivery only after confirming the target workspace, cadence, and permissions. <br>
Risk: The security scan reports execution of a helper script from another skill workspace. <br>
Mitigation: Inspect that helper path and replace it with a reviewed local implementation before deployment. <br>


## Reference(s): <br>
- [Claw News release page](https://clawhub.ai/russellfei/claw-news) <br>
- [Kimi API reference](references/kimi_api.md) <br>
- [MiniMax API reference](references/minimax_api.md) <br>
- [Claude API reference](references/claude_api.md) <br>
- [RSS sources](references/rss_sources.md) <br>
- [RSS setup guide](rss/SETUP.md) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, JSON, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown digests, JSON news data, and command-line configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write cache and digest files under the skill workspace and may post summaries through configured delivery channels.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
