## Description:

fastfish-hot fetches hot-topic news from api.pearktrue.cn, supports Feishu, DingTalk, and Telegram notifications, and helps configure real-time or scheduled pushes with keyword filtering.

This skill is ready for commercial/non-commercial use.

## Publisher:

[superxs777](https://clawhub.ai/user/superxs777)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to fetch trending topics and configure daily hot-news notifications to Feishu, DingTalk, or Telegram. It is also used to set filtering keywords, push schedules, and supporting local configuration for the fastfish-hot project.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installation runs third-party code and dependencies and may create persistent webhook-backed cron jobs.

Mitigation: Install only after reviewing the repository and dependencies, pin and verify the exact commit or release, run in a non-root isolated environment, and review each cron job before creation.

Risk: Webhook tokens and optional admin credentials could be exposed if entered or displayed in an untrusted setup path.

Mitigation: Enter credentials only in a private trusted setup path, avoid displaying .env contents or webhook values, and protect any enabled admin UI with an API key.

Risk: The skill depends on api.pearktrue.cn and external notification channels for fetching and pushing hot-topic content.

Mitigation: Use the skill only if the data source and selected messaging channels are trusted, and configure only the environment variables required for the intended channel.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/superxs777/skills/fastfish-hot)
- [ClawHub publisher profile](https://clawhub.ai/user/superxs777)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and optional JSON output from the underlying scripts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include credential setup guidance; should not reveal webhook tokens or .env contents.]

## Skill Version(s):

1.0.5 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
