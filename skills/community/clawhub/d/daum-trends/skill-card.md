## Description:

Daum Trends retrieves Daum real-time top 10 Korean search trends and one representative news headline per keyword for cron, Telegram, or Discord briefings.

This skill is ready for commercial/non-commercial use.

## Publisher:

[garibong-labs](https://clawhub.ai/user/garibong-labs)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to generate Korean Daum trend briefings for direct review or scheduled delivery to Telegram, Discord, or similar channels.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill makes outbound requests to Daum pages at runtime.

Mitigation: Install and schedule it only in environments where Daum network access and Korean trends notifications are intended.

Risk: Remote trend titles can be rendered in the default Markdown output.

Mitigation: Use plain or HTML output for downstream renderers, or add Markdown escaping before posting to Telegram, Discord, or similar channels.

Risk: Cron configuration can send scheduled announcements to public or shared channels.

Mitigation: Enable scheduled delivery only for channels where repeated public trend announcements are approved.

## Reference(s):

- [Daum homepage trend source](https://www.daum.net/)
- [Daum search results source](https://search.daum.net/search?w=tot&DA=RT1&rtmaxcoll=AIO,NNS,DNS&q=)
- [ClawHub skill page](https://clawhub.ai/garibong-labs/skills/daum-trends)
- [Publisher profile](https://clawhub.ai/user/garibong-labs)

## Skill Output:

**Output Type(s):** [Text, Markdown, HTML, Shell commands, Configuration guidance]

**Output Format:** [Plain text, Markdown, or HTML trend briefing]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Fetches live Daum pages at runtime; default Markdown output may include unescaped remote trend titles.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
