## Description: <br>
Helps HR teams review compensation decisions, compare bands and market signals, and precheck China payroll filing risks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ashley-aihr](https://clawhub.ai/user/ashley-aihr) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
HR teams use this skill to evaluate offer and band decisions, summarize market and internal compensation evidence, and precheck payroll, tax, social insurance, and housing fund filing readiness. It produces a structured decision, basis, missing information, risk summary, prioritized issues, next actions, and internal message drafts. <br>

### Deployment Geography for Use: <br>
China-oriented HR workflows; confirm applicability for each city, legal entity, and filing context. <br>

## Known Risks and Mitigations: <br>
Risk: The skill can process confidential employee compensation, payroll, national ID, and bank-detail fields. <br>
Mitigation: Use the minimum necessary fields, mask national ID and bank details where possible, and restrict access to inputs and outputs. <br>
Risk: Generated JSON and CSV packets may expose sensitive HR data if written to a shared or unmanaged folder. <br>
Mitigation: Choose a restricted output folder, limit sharing of generated files, and delete exported packets when no longer needed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ashley-aihr/compensation-repo) <br>
- [Project homepage](https://github.com/Ashley-AIHR/hrskill-compensation-module) <br>
- [China compensation policy knowledge base](references/china-compensation-policy-kb-2026.md) <br>
- [Compensation workflows](references/compensation-workflows.md) <br>
- [Dynamic market data architecture](references/dynamic-market-data-architecture.md) <br>
- [Real user scenario](references/real-user-scenario.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, CSV, shell commands, guidance] <br>
**Output Format:** [Structured Markdown guidance with optional JSON and CSV packet files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Optional COMP_EXPORT_PATH controls the local export path; generated files may contain confidential HR data.] <br>

## Skill Version(s): <br>
0.5.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
