## Description:

Fetches the latest AI Insight Daily RSS entries, formats them as a concise digest, and can push the digest to configured webhook channels.

This skill is ready for commercial/non-commercial use.

## Publisher:

[damomhd](https://clawhub.ai/user/damomhd)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and automation users use this skill to retrieve recent AI Insight Daily posts, generate a readable Markdown digest, and optionally distribute it through Bark, WeCom, Feishu, DingTalk, or generic webhook endpoints.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Crafted count or RSS URL values may cause unintended code execution in the fetch script.

Mitigation: Validate the count and RSS URL before use, and pass values to Python through arguments or environment data with a quoted heredoc.

Risk: Webhook URLs may include tokens that can be exposed in command output or logs.

Mitigation: Use webhook destinations you control and avoid printing webhook URL paths or tokens.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/damomhd/skills/aiinsight-daily-new)
- [AI Insight Daily RSS feed](https://justlovemaki.github.io/CloudFlare-AI-Insight-Daily/rss.xml)
- [AI Insight Daily publisher profile](https://github.com/justlovemaki)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration]

**Output Format:** [Markdown digest text with optional webhook JSON payloads]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Fetch count, RSS URL, and webhook destinations are configured through command arguments and environment variables.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
