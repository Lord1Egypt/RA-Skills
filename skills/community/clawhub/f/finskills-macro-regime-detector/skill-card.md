## Description:

Classify the current macroeconomic regime across six states using GDP, CPI, Fed Funds rate, yield curve, and credit spread data from the Finskills API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[finskills](https://clawhub.ai/user/finskills)

### License/Terms of Use:

MIT-0

## Use Case:

External users and financial-analysis agents use this skill to classify the current US macroeconomic regime, explain the supporting economic signals, and summarize portfolio allocation implications.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends macro-analysis requests to the external Finskills API using FINSKILLS_API_KEY.

Mitigation: Configure the API key only in the intended agent environment and avoid including private portfolio holdings, personal financial details, or other secrets in prompts.

Risk: Macro regime output can be incomplete or misleading if API data is delayed, unavailable, or interpreted as investment advice.

Mitigation: Treat the report as analytical guidance, review the cited economic signals, and confirm decisions with appropriate financial judgment before acting.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/finskills/skills/finskills-macro-regime-detector)
- [Finskills API](https://finskills.net)
- [Finskills macro regime detector homepage](https://github.com/finskills/macro-regime-detector)

## Skill Output:

**Output Type(s):** [text, markdown, API calls, guidance]

**Output Format:** [Markdown macro regime report with dashboard values, classification, rationale, watch triggers, and allocation implications]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires FINSKILLS_API_KEY and sends requests to the Finskills API.]

## Skill Version(s):

1.0.1 (source: server release metadata; artifact frontmatter reports 1.0.2)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
