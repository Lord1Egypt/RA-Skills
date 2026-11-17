## Description:

Provides stock K-line data retrieval, KDJ, MACD, BOLL, and moving-average technical indicators, capital-flow rankings, and concise buy, hold, or watch-style analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zaferliu](https://clawhub.ai/user/zaferliu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and analysts use this skill to fetch public market data, calculate common technical indicators, and generate informational stock-analysis summaries. The generated analysis is intended as technical reference material and not as investment advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Dependency versions are specified as minimums, which can allow future package changes to affect behavior.

Mitigation: Install the skill in an isolated Python environment and pin or lock dependencies before operational use.

Risk: Generated buy, hold, or watch-style analysis may be mistaken for investment advice.

Mitigation: Present the output as informational technical analysis only and require human review before making investment decisions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zaferliu/skills/eastmoney-tech-analysis)
- [Publisher profile](https://clawhub.ai/user/zaferliu)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, guidance]

**Output Format:** [Markdown, Python examples, command-line output, and optional JSON analysis results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses public Eastmoney market-data endpoints and Python dependencies for requests, pandas, and numpy.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
