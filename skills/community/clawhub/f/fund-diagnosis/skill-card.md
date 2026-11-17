## Description:

Provides single-fund diagnostic analysis for public mutual fund questions and returns a structured Markdown report covering overall judgment, holding considerations, and risk and return characteristics.

This skill is ready for commercial/non-commercial use.

## Publisher:

[financial-ai-analyst](https://clawhub.ai/user/financial-ai-analyst)

### License/Terms of Use:

MIT-0

## Use Case:

External users and financial-analysis agents use this skill to answer broad questions about a single public mutual fund, such as whether it is suitable to continue holding and what its risk and return profile looks like. It is not intended for multi-fund comparison, backtesting, portfolio optimization, or quantitative modeling workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Fund questions and the EM_API_KEY are sent to Eastmoney's API.

Mitigation: Install only when that data transfer is acceptable, keep the API key revocable, and keep the key out of logs, prompts, and shared files.

Risk: Returned fund diagnostics may be mistaken for investment advice.

Mitigation: Present the report as reference-only analysis and include a risk notice that it does not constitute investment advice.

Risk: Markdown reports may be saved locally by default and retained longer than intended.

Mitigation: Use --no-save for sensitive analyses or manage the generated report files according to the user's retention needs.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/financial-ai-analyst/skills/fund-diagnosis)
- [Eastmoney Miaoxiang service](https://ai.eastmoney.com/mxClaw)
- [Eastmoney fund-analysis API endpoint](https://ai-saas.eastmoney.com/proxy/)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Files, Shell commands, Guidance]

**Output Format:** [Markdown report, optionally saved as a local .md file]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The visible answer should use the API-returned Markdown as the primary content and should not invent a report when the API returns an error or empty body.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
