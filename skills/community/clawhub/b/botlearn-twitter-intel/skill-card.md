## Description:

Monitor Twitter/X to identify key opinion leaders, track emerging trends, analyze sentiment, detect bot activity, and deliver verified real-time intelligence reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[calvinxhk](https://clawhub.ai/user/calvinxhk)

### License/Terms of Use:

MIT

## Use Case:

Developers, analysts, and intelligence teams use this skill to scope Twitter/X monitoring requests, curate KOL and topic sources, filter noisy engagement, detect bot-amplified narratives, and produce structured briefings with confidence ratings and source attribution.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Twitter/X analysis can involve public social media data, platform API limits, and privacy expectations.

Mitigation: Use the skill only for appropriate public-platform analysis, define topic, time-window, language, and region scope, and ensure Twitter/X API access complies with platform terms and privacy expectations.

Risk: High engagement, single tweets, sarcasm, or incomplete thread context can lead to misleading credibility or sentiment judgments.

Mitigation: Require corroboration from independent sources, assess account credibility separately from engagement, inspect tone and thread context, and include confidence ratings with source attribution.

Risk: Bot networks or coordinated campaigns can make manufactured narratives appear organic.

Mitigation: Apply bot and coordination heuristics, separate raw from bot-filtered engagement metrics, and clearly flag suspected inauthentic amplification in the briefing.

Risk: Twitter/X discourse may not represent broader public opinion.

Mitigation: Frame findings as Twitter/X-specific and recommend cross-platform validation when broader opinion or decision support is needed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/calvinxhk/skills/botlearn-twitter-intel)
- [Twitter Intelligence Strategy](strategies/main.md)
- [Twitter Intelligence - API, Engagement Metrics & KOL Signals](knowledge/domain.md)
- [Twitter Intelligence - Best Practices](knowledge/best-practices.md)
- [Twitter Intelligence - Anti-Patterns](knowledge/anti-patterns.md)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown intelligence briefing with tables, bullet summaries, confidence ratings, source attribution, bot and inauthenticity assessment, and recommended actions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires user-provided topic, account, time-window, language, and region scope when those are material to the analysis.]

## Skill Version(s):

1.0.0 (source: server release metadata, target metadata, skill.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
