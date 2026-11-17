## Description:

Scrapes and summarizes AgResource grain newsletters with daily sales advice, price-impact sentiment analysis, trend tracking, and Telegram alerts on updates.

This skill is ready for commercial/non-commercial use.

## Publisher:

[brianppetty](https://clawhub.ai/user/brianppetty)

### License/Terms of Use:


## Use Case:

Developers and operators use this skill to collect AgResource newsletter content, summarize grain market updates, track price-impact sentiment over time, and surface sales-advice changes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release evidence reports plaintext fallback credentials for an AgResource account.

Mitigation: Remove the embedded password, rotate and invalidate exposed credentials, and require credentials from a protected secret mechanism before use.

Risk: The skill persistently stores authenticated newsletter content, screenshots, raw content files, summaries, and sentiment history locally.

Mitigation: Confirm local retention is permitted for the subscribed content and restrict, encrypt, or periodically delete stored files as appropriate.

Risk: Telegram alerts and scheduled scraping can redistribute subscribed newsletter-derived information automatically.

Mitigation: Review or disable Telegram delivery and cron jobs unless recipients, timing, and content retention have been approved.

## Reference(s):

- [ClawHub Agresource skill page](https://clawhub.ai/brianppetty/skills/agresource)
- [AgResource dashboard](https://agresource.com/dashboard/#/reports/daily)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, guidance]

**Output Format:** [Markdown summaries, JSON sentiment history, Telegram alert text, and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes local newsletter summaries, raw content, screenshots, and rolling sentiment history under ~/clawd/memory/agresource.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
