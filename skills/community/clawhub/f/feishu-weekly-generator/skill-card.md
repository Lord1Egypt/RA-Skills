## Description:

Generate professional weekly work reports for Feishu/Lark users by collecting work data from available sources such as git commits and creating formatted Markdown compatible with Feishu documents.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jiahui220](https://clawhub.ai/user/jiahui220)

### License/Terms of Use:

MIT-0

## Use Case:

Employees and developers use this skill to generate Feishu/Lark-compatible weekly work reports from a selected date range, optional git activity, and a chosen report template.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The bundled script has unsafe command execution behavior when collecting git history.

Mitigation: Review the script before use and avoid passing untrusted values to --git, --start, --end, or --output.

Risk: The script can overwrite files at the requested output path.

Mitigation: Write reports to a dedicated local working directory and inspect the output path before running.

Risk: Generated reports may expose confidential commit messages or internal work details.

Mitigation: Keep generated reports local until a reviewer has removed sensitive information.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jiahui220/skills/feishu-weekly-generator)
- [standard.md template](references/templates/standard.md)
- [detailed.md template](references/templates/detailed.md)
- [minimal.md template](references/templates/minimal.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration]

**Output Format:** [Markdown weekly report and command-line guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated reports may include git commit messages and internal work details; review content before sharing or uploading to Feishu.]

## Skill Version(s):

1.0.0 (source: release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
