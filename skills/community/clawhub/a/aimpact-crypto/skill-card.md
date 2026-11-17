## Description:

AIMPACT Crypto provides Chinese-language crypto morning reports, evening reports, 24-hour trend rankings, and curated news from configured AIMPACT and MetaEra API sources.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jamesmenews](https://clawhub.ai/user/jamesmenews)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to ask an agent for Chinese-language crypto briefings, trend rankings, and curated news summaries. It can also support optional scheduled delivery through already configured messaging channels.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Reports are based on configured crypto-news APIs and may contain time-sensitive or incomplete market information.

Mitigation: Treat reports as informational summaries and verify linked source material before making market, compliance, or operational decisions.

Risk: Optional scheduled delivery can send reports to already configured messaging recipients.

Mitigation: Configure the message tool or scheduler examples only when automatic delivery is intended, and verify target channels after setup.

Risk: The skill depends on curl access to agent.me.news API endpoints.

Mitigation: Confirm network access to the listed endpoints and review returned HTTP status codes or error summaries when requests fail.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/jamesmenews/skills/aimpact-crypto)
- [Publisher Profile](https://clawhub.ai/user/jamesmenews)
- [MetaEra AI Flash API](https://agent.me.news/skill/flash/list?page=1&size=20)
- [AIMPACT Crypto News API](https://agent.me.news/skill/aimpact/articles?page=1&size=20&category=crypto)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Chinese-language Markdown reports with source links and optional shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Top 10 news items by report type; optional delivery through configured messaging channels.]

## Skill Version(s):

0.8.1 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
