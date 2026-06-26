## Description: <br>
Atlas Argos Teste guides an agent acting as the autonomous ATLAS manager for the ARGOS crypto trading bot, covering operations, user and payment administration, marketing, Python maintenance, and Telegram reporting. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[felix1983](https://clawhub.ai/user/felix1983) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Operators of the ARGOS crypto trading bot use this skill to direct an agent through daily monitoring, incident response, user and payment administration, marketing activity, Python maintenance, and recurring owner reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill asks an agent to operate a live crypto trading bot with broad access to local files, processes, internet tools, and credentials. <br>
Mitigation: Run the agent under a restricted project user or sandbox and require approval before code changes, process restarts, package installs, or credential-dependent actions. <br>
Risk: The skill includes user and payment administration workflows that could affect access tiers, subscriptions, revenue records, or customer communications. <br>
Mitigation: Require human review for user promotions, demotions, payment changes, webhook changes, and any updates to payment or subscription records. <br>
Risk: The skill directs recurring Telegram reports and external messages that may expose user IDs, logs, revenue data, issue details, or operational status. <br>
Mitigation: Redact or minimize personal data, logs, revenue figures, and incident details before sending reports to Telegram or external AI tools. <br>
Risk: The skill includes public marketing and social posting workflows for Telegram, X, Reddit, YouTube, and TikTok. <br>
Mitigation: Require approval for public posts and verify that trading results, win rates, losses, and performance claims are accurate before publication. <br>
Risk: The skill contains restart, monitoring, cron, shell, and Python snippets that could change a production system if executed directly. <br>
Mitigation: Review commands in context, test changes before deployment, and keep logs or changelogs for code edits, restarts, and scheduled task changes. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/felix1983/atlas-argos-teste) <br>
- [Publisher profile](https://clawhub.ai/user/felix1983) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with bash commands, Python snippets, cron entries, tables, and message templates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs are written in PT-PT and may include operational instructions for local files, processes, Telegram Bot API calls, payment administration, and public posting workflows.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
