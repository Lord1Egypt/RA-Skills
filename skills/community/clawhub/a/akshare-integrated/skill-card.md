## Description:

Provides multi-market stock screening and risk-control suggestions using AKShare real-time data, intelligent scoring, and dynamic weighting.

This skill is ready for commercial/non-commercial use.

## Publisher:

[haosongyi-star](https://clawhub.ai/user/haosongyi-star)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and market-analysis users can use this skill to have an agent gather AKShare stock data, run multi-factor scoring, and produce informational screening, position-sizing, and risk-control guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can produce BUY, SELL, and position-size outputs that may be mistaken for financial advice.

Mitigation: Treat outputs as informational only and independently verify investment assumptions, data freshness, and suitability before acting.

Risk: The skill depends on live AKShare data and Python packages that may change or fail at runtime.

Mitigation: Install dependencies in an isolated environment with pinned versions, monitor data freshness, and validate fallback behavior before use.

## Reference(s):

- [Akshare Integrated ClawHub page](https://clawhub.ai/haosongyi-star/skills/akshare-integrated)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with shell commands, Python snippets, API examples, and JSON result examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include stock actions, scores, position suggestions, real-time price fields, evidence levels, and risk-control thresholds.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
