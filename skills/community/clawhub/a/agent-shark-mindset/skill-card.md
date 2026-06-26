## Description: <br>
Agent Shark Mindset guides OpenClaw agents through scheduled market scans, audience-growth content, Telegram signal publishing, and weekly revenue audits. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[georges91560](https://clawhub.ai/user/georges91560) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to configure an OpenClaw agent that produces finance-focused market briefs, channel content, Telegram posts, and revenue audit reports. It is intended for agent workflows that combine public market data, promotional content, and owner-facing performance summaries. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can autonomously publish market-related trading signals and promotional content to Telegram using bot credentials. <br>
Mitigation: Use test or private channels first, keep publishing in manual-review mode where possible, and grant the Telegram bot only the minimum channel permissions required. <br>
Risk: Scheduled jobs may write recurring financial-signal, revenue, memory, strategy, and learning files in the workspace. <br>
Mitigation: Verify the cron messages before enabling them and periodically inspect or clean CASHFLOW, memory, STRATEGY, and .learnings outputs. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/georges91560/agent-shark-mindset) <br>
- [Polymarket public CLOB API](https://clob.polymarket.com) <br>
- [Telegram Bot API](https://api.telegram.org) <br>
- [Reddit r/algotrading public JSON](https://www.reddit.com/r/algotrading.json) <br>
- [Reddit r/CryptoCurrency public JSON](https://www.reddit.com/r/CryptoCurrency.json) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown instructions, Telegram-ready messages, cron configuration, JSON log updates, and workspace files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Telegram channel identifiers and bot credentials for publishing workflows.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata; artifact frontmatter says 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
