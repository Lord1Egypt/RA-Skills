## Description:

Analyze financial news, announcements, and research reports for sentiment, impact horizon, importance, and news category.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gbabyzs](https://clawhub.ai/user/gbabyzs)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and finance analysts use this skill to ask an agent for a structured sentiment snapshot of market news for a stock code, including positive, neutral, and negative counts, a sentiment score, key events, and expected impact.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The declared third-party dependencies are unpinned and unused in the current artifact.

Mitigation: Remove unused dependencies before installation, or pin and review them if live data collection features are added.

Risk: The current Python helper returns sample sentiment data that could be mistaken for live market analysis.

Mitigation: Clearly label sample outputs and integrate validated news sources and NLP models before using the result for financial decisions.

Risk: Chinese-language documentation and output may not fit every deployment audience.

Mitigation: Confirm the intended user language and localize documentation or output labels where needed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/gbabyzs/skills/aigc-news-sentiment)

## Skill Output:

**Output Type(s):** [text, code, guidance]

**Output Format:** [Markdown guidance and Python dictionary/JSON-like sentiment results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns a compact sentiment summary for a supplied stock code; current artifact behavior uses sample data and notes that live news crawling and NLP integration are still needed.]

## Skill Version(s):

1.0.0 (source: release evidence and skill.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
