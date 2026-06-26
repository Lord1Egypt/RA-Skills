## Description: <br>
Use when user wants to build financial models, DCF analysis, valuation, sensitivity analysis, e-commerce business planning, investment decisions, or project finance assessments. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[simoncai519](https://clawhub.ai/user/simoncai519) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees, external users, and developers use this skill to structure financial modeling workflows, run simple DCF valuation calculations, and prepare valuation workbooks from user-provided assumptions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Financial valuation outputs may be incomplete or misleading if inputs, assumptions, or formulas are wrong. <br>
Mitigation: Review assumptions and source financials carefully, sanity-check outputs against other valuation methods, and do not treat results as professional financial advice. <br>
Risk: Workbook generation writes to the requested output path and could overwrite an existing file. <br>
Mitigation: Choose output paths deliberately and review the destination before running the script. <br>
Risk: The workbook generator depends on the xlsxwriter Python package. <br>
Mitigation: Install dependencies only from trusted package sources and use a reviewed or pinned Python environment when possible. <br>


## Reference(s): <br>
- [Financial Modeling Methodology](references/methodology.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Files] <br>
**Output Format:** [Markdown guidance with optional shell commands and generated Excel workbook files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reads user-provided JSON inputs and may write an .xlsx workbook to a user-selected output path.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
