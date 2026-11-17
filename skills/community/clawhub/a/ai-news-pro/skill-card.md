## Description:

AI News Pro produces AI morning and evening briefings, 24-hour hot-news rankings, and curated AI news sorted by AI score, with optional scheduled delivery.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jamesmenews](https://clawhub.ai/user/jamesmenews)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to request Chinese-language AI news briefings, hot-news rankings, and curated updates from configured ME News API sources. It can also provide optional scheduled push delivery when OpenClaw message tooling and channel credentials are already configured outside the skill.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Optional OS-level scheduled tasks can continue running unattended and sending reports after setup.

Mitigation: Enable scheduled delivery only after confirming the message destination and documenting how to disable the cron or Windows Task Scheduler entry.

Risk: Push delivery depends on externally configured message tooling and channel credentials.

Mitigation: Keep channel credentials outside the skill and verify OpenClaw message configuration before enabling push delivery.

## Reference(s):

- [AI News Pro ClawHub listing](https://clawhub.ai/jamesmenews/skills/ai-news-pro)
- [AI News Pro publisher profile](https://clawhub.ai/user/jamesmenews)
- [MetaEra AI flash API](https://agent.me.news/skill/flash/list?page=1&size=20&category=ai)
- [AI news API](https://agent.me.news/skill/aimpact/articles?page=1&size=20&category=ai)
- [OpenClaw news API](https://agent.me.news/skill/aimpact/articles?page=1&size=20&category=openclaw)
- [AI industry events API](https://agent.me.news/skill/aimpact/events)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown news briefing with source links and optional shell scheduler examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Chinese-language reports are grouped by AI topic category, limited to about 10 to 12 items, and end with a brief trend observation.]

## Skill Version(s):

0.9.1 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
