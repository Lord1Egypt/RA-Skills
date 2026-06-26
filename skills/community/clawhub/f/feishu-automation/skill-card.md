## Description: <br>
Automates Feishu (Lark) document workflows, app-to-app data syncing, report generation, and batch operations across documents, wikis, bitables, and cloud storage. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Hejk](https://clawhub.ai/user/Hejk) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operations teams use this skill to automate Feishu/Lark document, wiki, Bitable, drive, and reporting workflows, including batch updates, migrations, backups, and generated reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can be used with broad Feishu access across documents, wikis, bitables, and drive folders. <br>
Mitigation: Grant the narrowest Feishu app scopes and folder or document access needed for the workflow. <br>
Risk: Batch, migration, and backup workflows can affect many documents or export sensitive workspace content. <br>
Mitigation: Run dry-run modes first, target specific tokens where possible, and review generated content before applying changes. <br>
Risk: Real Feishu app secrets in checked-in configuration could expose workspace access. <br>
Mitigation: Keep production credentials in environment variables or a secret manager instead of repository config files. <br>


## Reference(s): <br>
- [Weekly Report Automation Workflow](references/weekly_report_workflow.md) <br>
- [Feishu API Patterns](references/feishu_api_patterns.md) <br>
- [Error Handling Guide](references/error_handling.md) <br>
- [Best Practices for Feishu Automation](references/best_practices.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with Python scripts, YAML configuration examples, reusable templates, and shell command examples.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update Feishu documents, generated Markdown reports, local backup files, and JSON reports when users run the provided scripts.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
