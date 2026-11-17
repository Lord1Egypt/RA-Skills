## Description:

Forecast Valuation generates Excel financial forecast and valuation workbooks with historical statements, assumptions, DCF valuation, comparable-company analysis, sensitivity analysis, and football-field valuation views.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cgxxxxxxxxxxxx](https://clawhub.ai/user/cgxxxxxxxxxxxx)

### License/Terms of Use:

MIT-0

## Use Case:

Agents assisting financial analysts use this skill to generate local Excel valuation models for companies, including forecast assumptions, DCF outputs, comparable-company valuation, and sensitivity checks. Users should verify all financial data, formulas, and assumptions before using outputs for decisions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Gangtise and Tushare credentials may be stored in plaintext config.json.

Mitigation: Use temporary or environment-managed credentials, and do not enter real credentials unless plaintext local storage is acceptable in the deployment environment.

Risk: Hard-coded example financial data and formulas can make generated workbooks look like professional analysis.

Mitigation: Verify or replace all financial data, valuation assumptions, and formulas before relying on the workbook; do not treat outputs as investment advice.

Risk: Some advertised upload or API features were not implemented in the inspected scripts.

Mitigation: Confirm required integrations are implemented and tested before depending on those features in a workflow.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/cgxxxxxxxxxxxx/skills/forecast-valuation)
- [Publisher Profile](https://clawhub.ai/user/cgxxxxxxxxxxxx)
- [Skill README](docs/README.md)

## Skill Output:

**Output Type(s):** [Files, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Excel workbook (.xlsx), terminal status text, and optional JSON configuration]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generates a local valuation workbook; the default output path is /root/.openclaw/workspace unless an output path is supplied.]

## Skill Version(s):

1.0.0 (source: frontmatter, release evidence, docs/README.md)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
