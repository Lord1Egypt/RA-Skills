## Description: <br>
Generate import-ready data from user-provided Excel or CSV import templates based on the customer's described business scenario. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[huahuaweiwei](https://clawhub.ai/user/huahuaweiwei) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operations teams use this skill to inspect uploaded Excel or CSV import templates and generate matching sample, test, or initialization rows for a described business scenario. It helps preserve sheet choice, column names, column order, and visible formatting expectations while making assumptions explicit. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated rows can be incorrect or unsuitable for a production import if the template rules, required code dictionaries, or business scenario are incomplete. <br>
Mitigation: Review the generated rows, stated assumptions, detected headers, and row counts before loading them into a real business system. <br>
Risk: Uploaded spreadsheet or CSV templates may contain sensitive data that the agent can read while preparing matching output. <br>
Mitigation: Avoid using sensitive production data unless the runtime is trusted, and provide sanitized templates when possible. <br>


## Reference(s): <br>
- [Generation Guidelines](references/generation-guidelines.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with tables or fenced CSV blocks, plus generated workspace files when appropriate] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Summarizes chosen sheet, detected headers, row count, and material assumptions; may create a new output file instead of overwriting the source template.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
