## Description:

Guides agents using the bim CLI to inspect, export, and edit AEC files and Revit models.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hellohowareyouhaveaniceday](https://clawhub.ai/user/hellohowareyouhaveaniceday)

### License/Terms of Use:

MIT-0

## Use Case:

Architects, engineers, and AEC developers use this skill to work with drawing sets, BIM files, and Revit models through a Windows CLI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installing the CLI runs a downloaded installer and updates the user's PATH.

Mitigation: Get the user's approval first and confirm they trust bimcli.com and want a per-user installation.

Risk: Revit commands and scripts can change an open model or disrupt the user's session.

Mitigation: Keep work read-only unless changes are requested; use preflight, compile-only, or rollback where available and review model-modifying scripts before execution.

Risk: Model-derived PDF-BIM sidecar values can differ from the printed drawing sheets.

Mitigation: Treat printed sheets as authoritative and label unconfirmed model-derived values.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/hellohowareyouhaveaniceday/skills/bim-cli)
- [bim-cli homepage](https://bimcli.com)
- [PDF driver notes](https://bimcli.com/pdf/llms.txt)
- [Revit driver notes](https://bimcli.com/revit/llms.txt)
- [Bundled PDF reference](artifact/references/pdf.md)
- [Bundled Revit reference](artifact/references/revit.md)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Code, Configuration instructions]

**Output Format:** [Markdown with command and code snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Windows 10/11; some operations require installed host applications such as Revit.]

## Skill Version(s):

1.1.0 (source: skill frontmatter and ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
