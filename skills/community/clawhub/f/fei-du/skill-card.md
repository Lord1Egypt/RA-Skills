## Description:

Fei Du helps agents extract insights, recognize patterns, identify anomalies, compare items, and summarize trends from supplied data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lt8899789](https://clawhub.ai/user/lt8899789)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent builders use this skill to perform Chinese-language data analysis workflows, including insight extraction, trend recognition, anomaly detection, and comparison reporting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may ask an agent to use separately installed aggregation skills for finance, search, GitHub, or image-analysis workflows.

Mitigation: Review those separately installed skills and their data-access, reliability, and security properties before using them together.

Risk: The bundled analysis behavior uses simple statistical and string-matching methods that can miss context or produce misleading conclusions for high-stakes decisions.

Mitigation: Treat results as decision-support summaries and validate important findings against authoritative data and domain review.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, json, guidance]

**Output Format:** [Markdown or JSON-style analysis summaries with insights, patterns, anomalies, trends, comparisons, and recommendations.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include confidence values, forecasts, timestamps, and recommendation fields.]

## Skill Version(s):

1.0.35 (source: server release evidence and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
