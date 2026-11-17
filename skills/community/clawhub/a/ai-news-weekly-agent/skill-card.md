## Description:

Generates a weekly AI report with OpenClaw top skills, official announcements, industry news, open-source updates, and a capped research-paper ratio in Markdown format.

This skill is ready for commercial/non-commercial use.

## Publisher:

[matilda-grifin](https://clawhub.ai/user/matilda-grifin)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to generate a traceable weekly AI digest from configured news, RSS, research, open-source, and OpenClaw leaderboard sources. It is useful when a user needs a structured Markdown report with source links, publish dates, and optional LLM-generated Chinese analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can fetch configured RSS/news sources and follow article links that may include untrusted web content.

Mitigation: Use trusted sources only and review generated reports before sharing them.

Risk: Selected fetched excerpts and report content may be sent to the configured LLM provider when LLM generation is enabled.

Mitigation: Provide API keys through protected environment injection and run only with approved LLM endpoints.

Risk: Relaxing endpoint or transport controls can increase exposure to unsafe destinations or insecure connections.

Mitigation: Avoid --allow-insecure-ssl and --allow-custom-llm-endpoint unless necessary, and extend LLM_ALLOWED_HOSTS only for trusted hosts.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/matilda-grifin/skills/ai-news-weekly-agent)
- [Publisher Profile](https://clawhub.ai/user/matilda-grifin)
- [Source Feed Configuration](sources.json)
- [Project Overview](README.md)
- [Sample Weekly Report](daily_docs/ai_weekly_20260323.md)

## Skill Output:

**Output Type(s):** [markdown, text, shell commands, configuration, guidance]

**Output Format:** [Markdown report written to daily_docs/ai_weekly_YYYYMMDD.md, with source links, publish dates, summaries, and optional webhook notification text.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The report defaults to a 168-hour window, caps research papers at 20 percent by default, preserves source attribution, and records fetch errors in the generated Markdown.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
