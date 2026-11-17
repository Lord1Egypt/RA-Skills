## Description:

Advanced automation workflows for Feishu (Lark) productivity suite, including document workflows, cross-app data sync, report generation, and batch operations across documents, wikis, bitables, and cloud storage.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hejk](https://clawhub.ai/user/hejk)

### License/Terms of Use:


## Use Case:

Developers and operations teams use this skill to automate Feishu/Lark document, wiki, Bitable, and drive workflows for reporting, backups, migrations, and batch updates.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: High-impact document, wiki, table, move, restore, or sharing automation can alter production Feishu content.

Mitigation: Run dry-runs first, require explicit approval before production execution, scope Feishu app permissions to the exact workflow, and keep backups before write or migration operations.

Risk: Some bundled scripts are demo stubs and can report success without performing real Feishu API operations.

Mitigation: Treat scripts as examples until real Feishu API behavior is verified and placeholder logic is replaced or reviewed for the target workflow.

Risk: Configuration examples include credential-shaped fields that could lead users to place real secrets in YAML files.

Mitigation: Use environment variables or a secrets manager for real credentials and avoid committing populated configuration files.

## Reference(s):

- [Feishu Automation Skill Page](https://clawhub.ai/hejk/skills/feishu-automation)
- [Weekly Report Automation Workflow](references/weekly_report_workflow.md)
- [Feishu API Patterns](references/feishu_api_patterns.md)
- [Error Handling Guide](references/error_handling.md)
- [Best Practices for Feishu Automation](references/best_practices.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with code snippets, shell commands, configuration examples, and generated document/report content]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce local Markdown, JSON reports, Feishu document content, and dry-run previews depending on the selected workflow.]

## Skill Version(s):

1.0.0 (source: server evidence release.version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
