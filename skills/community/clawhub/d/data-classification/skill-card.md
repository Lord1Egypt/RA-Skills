## Description: <br>
Classifies single data field names, field lists, and database SQL/DDL into general data classification and grading labels, including GB/T 43697-2024 style labels and JR/T 0197-2020 financial data labels. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[liangzaiz666](https://clawhub.ai/user/liangzaiz666) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, data governance teams, and compliance reviewers use this skill to produce first-pass classifications for database fields and SQL schemas. It helps identify general data categories, grading levels, financial labels, confidence, and review points before business-owner validation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Schema, DDL, or field-list inputs may contain sensitive metadata or embedded secrets. <br>
Mitigation: Provide schema and DDL instead of real data rows where possible, and remove secrets before running classification. <br>
Risk: Generated CSV outputs may retain sensitive schema metadata after the review task is complete. <br>
Mitigation: Review generated CSV files for sensitivity and delete them when they are no longer needed. <br>
Risk: Classification results are suggestions and may not be final regulatory determinations. <br>
Mitigation: Route uncertain, high-impact, or low-confidence classifications to the relevant business owner or compliance reviewer. <br>


## Reference(s): <br>
- [General data classification rules](references/general-rules.md) <br>
- [Financial dual-label workflow](references/financial-dual-label.md) <br>
- [JR/T 0197-2020 Appendix A compact table](references/jrt0197-appendix-a-compact.md) <br>
- [JR/T 0197-2020 Appendix A full CSV](references/jrt0197-appendix-a-full.csv) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Markdown, Files, JSON] <br>
**Output Format:** [Markdown field-level tables, with optional CSV or JSON output from the helper script] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes coverage counts, confidence, review notes, and financial labels when the scenario is financial.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
