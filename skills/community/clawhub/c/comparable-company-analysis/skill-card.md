## Description:

A financial analysis skill for A-share listed companies that calls an Eastmoney comparable-company API and generates a themed Excel report comparing operating, financial, valuation, and statistical benchmark metrics.

This skill is ready for commercial/non-commercial use.

## Publisher:

[financial-ai-analyst](https://clawhub.ai/user/financial-ai-analyst)

### License/Terms of Use:

MIT-0

## Use Case:

External users and financial analysts use this skill to compare a single A-share listed company with peers across business, finance, and valuation dimensions. It is intended for rapid fundamental analysis and screening support, not as investment advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated Excel workbooks can include active formulas from API-controlled data.

Mitigation: Treat generated workbooks as untrusted, inspect them before use, and open them with spreadsheet protections enabled until formula sanitization is added.

Risk: The skill requires an Eastmoney EM_API_KEY for remote API access.

Mitigation: Provide the key only through the EM_API_KEY environment variable and avoid storing it in prompts, logs, code, or generated files.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/financial-ai-analyst/skills/comparable-company-analysis)
- [ClawHub publisher profile](https://clawhub.ai/user/financial-ai-analyst)
- [Eastmoney Miaoxiang account and API key page](https://ai.eastmoney.com/mxClaw)
- [Comparable-company analysis API endpoint](https://ai-saas.eastmoney.com/proxy/app-robo-advisor-api/assistant/comparable-company-analysis)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files]

**Output Format:** [Markdown guidance, JSON API responses, shell commands, and local XLSX workbook files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires EM_API_KEY and writes generated Excel reports under miaoxiang/comparable_company_analysis by default.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
