## Description: <br>
Completes a smart-store work-order retrospective workflow by pulling Furcas ticket data, importing it into Feishu Bitable, and creating or updating Feishu retrospective documents with summary statistics. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[runkecheng](https://clawhub.ai/user/runkecheng) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Operations, support, and engineering teams use this skill to run monthly work-order retrospectives, consolidate ticket data into Feishu Bitable, and generate review documents for follow-up analysis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can modify or delete live Feishu business data while importing ticket data and updating retrospective documents. <br>
Mitigation: Run it only in the intended Feishu/Furcas workspace, verify APP_TOKEN, TABLE_ID, DOC_ID, MONTH, CSV_PATH, and the active Feishu user before execution, and back up or export the target Bitable before import. <br>
Risk: The workflow depends on sensitive Furcas cookies and Feishu OAuth token files. <br>
Mitigation: Keep credentials in environment variables or local token storage, do not share cookies or UAT token files, and rotate credentials if they are exposed. <br>
Risk: The security review found limited confirmation and rollback safeguards for live data changes. <br>
Mitigation: Prefer adding dry-run, explicit confirmation, and backup steps before delete or PATCH operations. <br>


## Reference(s): <br>
- [Data Mapping](references/data_mapping.md) <br>
- [Bitable Schema](references/bitable-schema.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, code] <br>
**Output Format:** [Markdown instructions with shell commands, environment variables, and Feishu operation parameters] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses Furcas cookies, Feishu OAuth token files, month/date inputs, CSV paths, Bitable identifiers, and document identifiers supplied by the user or environment.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
