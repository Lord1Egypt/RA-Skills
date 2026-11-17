## Description:

Parallel fetches AI news from 36Kr and GeekPark, summarizes the top 10 items, and delivers a structured daily brief in Markdown via Telegram.

This skill is ready for commercial/non-commercial use.

## Publisher:

[warrior156006050](https://clawhub.ai/user/warrior156006050)

### License/Terms of Use:

MIT-0

## Use Case:

Users who follow AI news use this skill to collect recent items from 36Kr and GeekPark and receive a concise Markdown daily brief. It is suitable when the Telegram destination is reviewed and configured for the intended recipient.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends the daily brief to a fixed Telegram recipient named warrior.

Mitigation: Use it only if warrior is the intended recipient, or modify the destination so it is user-configured and confirmed before any Telegram message is sent.

Risk: Security evidence flags the release as suspicious because delivery is not user-controlled.

Mitigation: Review before installing and confirm the Telegram recipient against the intended deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/warrior156006050/skills/ai-daily-brief)
- [36Kr AI channel](https://www.36kr.com/information/AI/)
- [GeekPark AI column](https://www.geekpark.net/column/304)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown daily brief with a headline, core points, and a 2-3 sentence summary for each selected item]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Top 10 latest AI news items from configured sources; delivery is via Telegram.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
