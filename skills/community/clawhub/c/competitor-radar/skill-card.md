## Description:

Competitor Radar monitors competitor blog RSS feeds, GitHub releases, and Hacker News mentions, uses AI scoring to rank important updates, and generates a structured Markdown report.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xiaohuaishu](https://clawhub.ai/user/xiaohuaishu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, product teams, and market analysts use this skill to monitor configured competitors and produce concise Markdown reports of recent product, release, and community discussion signals.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A hardcoded LLM API key is shipped in the artifact.

Mitigation: Remove the embedded key, rotate the exposed credential, and require users to provide approved credentials through a local secret or environment configuration before enabling AI scoring.

Risk: Custom RSS feed URLs are accepted without validation.

Mitigation: Restrict configuration to approved public HTTPS feed destinations and review competitor feed entries before running the skill.

Risk: Collected titles are sent to the configured local LLM gateway when AI scoring is enabled.

Mitigation: Use --no-ai unless the local gateway, model, and data-sharing posture are approved for the monitored content.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/xiaohuaishu/skills/competitor-radar)
- [Publisher profile](https://clawhub.ai/user/xiaohuaishu)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown report with console status text and optional report file output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Ranks collected items by importance and includes source links, dates, and concise reasons when AI scoring is enabled.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
