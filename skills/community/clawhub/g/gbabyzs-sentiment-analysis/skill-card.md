## Description:

Analyzes stock-related social media sentiment signals and returns sentiment scores, trend indicators, discussion heat, and bot-detection style metrics.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gbabyzs](https://clawhub.ai/user/gbabyzs)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and finance-focused agents can use this skill to produce stock social-sentiment summaries from Chinese investor-community sources. Current outputs should be treated as test or illustrative sentiment data unless the implementation is replaced with real data collection and NLP analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The implementation advertises stock sentiment analysis while currently returning random simulated financial metrics.

Mitigation: Treat outputs as test data only; do not use them for trading or financial decisions until real data-source handling, NLP analysis, dependency pinning, and output validation are added and reviewed.

Risk: The artifact lists data and NLP dependencies without pinned versions.

Mitigation: Install in an isolated environment and pin reviewed dependency versions before operational use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/gbabyzs/skills/gbabyzs-sentiment-analysis)
- [Publisher profile](https://clawhub.ai/user/gbabyzs)

## Skill Output:

**Output Type(s):** [text, markdown, code, guidance]

**Output Format:** [Markdown guidance and Python dictionary-style sentiment results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns simulated stock sentiment fields such as sentiment_score, sentiment_level, bull_ratio, bear_ratio, hotness, updated timestamp, and note.]

## Skill Version(s):

1.0.0 (source: server release evidence and skill.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
