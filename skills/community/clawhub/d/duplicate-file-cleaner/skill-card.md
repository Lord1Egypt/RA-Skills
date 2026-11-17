## Description:

Scans user-selected directories for exact duplicate files, produces structured duplicate reports, and helps an agent suggest cautious cleanup actions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ludiansheng](https://clawhub.ai/user/ludiansheng)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to find exact duplicate files in directories the user chooses, summarize reclaimable disk space, and prepare cautious file-retention or deletion guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Cleanup guidance may lead to unintended file loss if duplicate reports are acted on without review.

Mitigation: Review the report before deleting files, prefer backup-or-move workflows first, and require explicit confirmation for deletion scripts.

Risk: Broad scans can expose sensitive file paths or include directories that the user did not intend to inspect.

Mitigation: Scan only user-selected directories and avoid system directories or broad home-directory scans unless that scope is explicit.

## Reference(s):

- [File Organization Best Practices Guide](references/file-organization-guide.md)
- [ClawHub Skill Page](https://clawhub.ai/ludiansheng/skills/duplicate-file-cleaner)
- [ClawHub Publisher Profile](https://clawhub.ai/user/ludiansheng)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON report interpretation]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The bundled scanner can write a JSON report to a user-specified output path.]

## Skill Version(s):

1.0.0 (source: server release metadata and manifest.md)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
