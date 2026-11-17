## Description:

Community sentiment via Gate-News MCP, X/Twitter-first. Use for social discussion, KOL takes, or opinion on a coin or topic.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gaixianggeng](https://clawhub.ai/user/gaixianggeng)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to summarize crypto community sentiment and X/Twitter discussion around a coin, topic, or broad market prompt. The skill is intended for social-sentiment reporting, not financial advice or price prediction.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Users may treat community sentiment as financial advice or a price prediction.

Mitigation: State that results are social chatter, present sentiment as non-predictive, and include the skill's non-investment-advice limitation.

Risk: Coverage is X/Twitter-focused and may omit Reddit, Discord, or Telegram discussion.

Mitigation: Label reports as X/Twitter-only unless supported UGC data is available, and note unavailable platforms in the output.

Risk: Ambiguous prompts may route to this skill when the user wanted news, fundamentals, or price-move analysis.

Mitigation: Use the routing rules to redirect news, coin analysis, and price-move questions to the appropriate dedicated skill.

Risk: Required Gate-News MCP tools may be unavailable or return partial data.

Mitigation: Degrade gracefully by reporting available dimensions, clearly marking missing sections, or returning a concise failure when all required tools fail.

## Reference(s):

- [Gate News Community Scan Runtime Rules](references/gate-runtime-rules.md)
- [Info & News Common Runtime Rules](references/info-news-runtime-rules.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown community sentiment report with tables and short takeaways]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Labels platform coverage, notes missing data, and includes a non-investment-advice limitation.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
