## Description:

Structured, multi-dimensional company investment research framework for AI agents and human analysts that turns scattered company information into a consistent investment memo.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dufu2000](https://clawhub.ai/user/dufu2000)

### License/Terms of Use:


## Use Case:

AI agents, analysts, and investment teams use this skill to evaluate public or late-stage private companies, compare peers, and produce structured investment memos with recommendation, valuation, financial, governance, and risk sections.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Investment conclusions may be misleading if based on stale, incomplete, or uncited company data.

Mitigation: Use current filings, financial data, and reputable sources; check data dates and cite key figures in the memo.

Risk: Illustrative filing, web, or financial API examples may make external requests or write local outputs when adapted by a user.

Mitigation: Run any adapted examples only in a controlled project directory and confirm API requests, credentials, and output paths before execution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/dufu2000/skills/company-investment-research)
- [Investment Analysis Framework Reference](references/analysis-framework.md)
- [Investment Research Report Template](references/report-template.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown investment memo framework with optional inline shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces structured analysis prompts, checklists, and memo sections; users should supply current company data and cite sources for financial claims.]

## Skill Version(s):

0.3.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
