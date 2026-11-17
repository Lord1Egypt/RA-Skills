## Description:

Daily Tech helps an agent produce a concise daily technology digest focused on AI, large language models, OpenClaw, robotics, open source projects, and international technology news.

This skill is ready for commercial/non-commercial use.

## Publisher:

[foxxc](https://clawhub.ai/user/foxxc)

### License/Terms of Use:

MIT-0

## Use Case:

Agents and end users use this skill to request or schedule a daily technology and AI news roundup. It is intended for concise human-facing summaries from Chinese and English technology sources, with optional recurring delivery to Feishu.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Enabling scheduled delivery creates persistent recurring OpenClaw activity through a Feishu cron job.

Mitigation: Confirm the destination channel before enabling the schedule, and ensure the operator knows how to list and remove the cron job if notifications are no longer wanted.

## Reference(s):

- [Daily Tech on ClawHub](https://clawhub.ai/foxxc/skills/daily-tech)
- [TopHub Juejin AI Weekly Hot List](https://tophub.today/n/rYqoXz8dOD)
- [TopHub QbitAI Daily Latest](https://tophub.today/n/MZd7azPorO)
- [TopHub MIT Technology Review](https://tophub.today/n/7GdabqLeQy)
- [TopHub 36Kr 24-Hour Hot List](https://tophub.today/n/Q1Vd5Ko85R)
- [The Verge RSS Feed](https://www.theverge.com/rss/index.xml)
- [TechCrunch RSS Feed](https://techcrunch.com/feed/)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown digest with concise categorized items and optional inline shell command for scheduling]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The digest is normally 5-10 items and uses ====== as a separator.]

## Skill Version(s):

1.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
