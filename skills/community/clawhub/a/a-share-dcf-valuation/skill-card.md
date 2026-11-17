## Description:

DCF valuation modeling for A-share listed companies. Pass stock code to automatically fetch financial data, calculate WACC, run conservative/base/optimistic three-scenario DCF valuation, generate sensitivity analysis matrix, and output complete Markdown report (in Chinese). Applicable to any A-share listed company valuation analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[laigen](https://clawhub.ai/user/laigen)

### License/Terms of Use:

MIT-0

## Use Case:

External users and finance-oriented agent workflows use this skill to run DCF valuation analysis for A-share listed companies from a stock code. The skill fetches market and financial data, calculates WACC, evaluates conservative/base/optimistic cases, and produces a Chinese Markdown valuation report.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Credential handling needs review because the skill requires a Tushare token and the documented verification command expands the token into the command line.

Mitigation: Use a temporary environment variable or secret manager, avoid putting the token in a global shell profile, and avoid commands that expose the token in process arguments.

Risk: Dependency and execution practices need review before installation.

Mitigation: Install in a dedicated virtual environment, review dependency sources, and pin versions before using the skill in a production workflow.

Risk: The valuation result depends on Tushare data availability and model assumptions, and may be misleading if treated as investment advice.

Mitigation: Use only intended A-share tickers, verify generated report paths and data freshness, and keep the report's financial disclaimer visible to users.

## Reference(s):

- [Tushare](https://tushare.pro)
- [ClawHub skill page](https://clawhub.ai/laigen/skills/a-share-dcf-valuation)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Chinese Markdown report with terminal progress text and report path]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires an A-share stock code and a Tushare token; writes a report under the workspace reports directory.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
