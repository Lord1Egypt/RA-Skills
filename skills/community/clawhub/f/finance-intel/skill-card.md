## Description:

财经情报局 is a Chinese-language finance intelligence skill that helps agents gather finance news, classify sentiment and impact, map related stocks, and draft investment briefing references.

This skill is ready for commercial/non-commercial use.

## Publisher:

[if530770](https://clawhub.ai/user/if530770)

### License/Terms of Use:

MIT-0

## Use Case:

External users and analysts use this skill to request Chinese-language market news briefings for A-share, Hong Kong, and U.S. equities, with keyword filtering, sentiment labels, impact levels, and related-stock context. Outputs are decision-support references and should not be treated as investment advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Financial sentiment labels, impact levels, and operation suggestions may be incomplete or misleading.

Mitigation: Review conclusions manually and treat generated briefings as informational references, not investment advice.

Risk: The included fetch logic appears incomplete despite listing many sources, which may lead to empty, stale, or partial news coverage.

Mitigation: Confirm source availability and supplement the briefing with verified market data before relying on it.

Risk: The skill writes local cache and report files under finance-news by default.

Mitigation: Run it in a controlled workspace, use --no-save when persistence is not desired, and review generated files before sharing.

## Reference(s):

- [Sentiment Analysis Rules and Stock Mapping](artifact/references/sentiment-rules.md)
- [Finance Source Configuration](artifact/references/sources-config.md)
- [Finance Intel Skill Page](https://clawhub.ai/if530770/skills/finance-intel)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown briefings with JSON news data and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write local cache and report files under finance-news unless --no-save is used.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
