## Description:

Batch converts legacy Microsoft Office .doc and .xls files to modern .docx and .xlsx formats, using Word COM automation for .doc files and Python libraries for .xls files.

This skill is ready for commercial/non-commercial use.

## Publisher:

[longjf25](https://clawhub.ai/user/longjf25)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to convert individual files or batches of legacy Office documents into modern Office formats during document migration or modernization work.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The Word conversion path opens legacy .doc files through Microsoft Word, which can expose users to active-content or macro risk in untrusted documents.

Mitigation: Only process trusted documents, or run the Word conversion path in an isolated Windows account or VM with Office macros and active content disabled.

Risk: The skill depends on Python packages for spreadsheet conversion.

Mitigation: Install dependencies in a virtual environment and pin package versions before operational use.

Risk: Batch conversion may overwrite existing output files.

Mitigation: Keep backups or write converted files to a separate output directory when preserving existing .docx or .xlsx files matters.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/longjf25/skills/doc-xls2docx-xlsx)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Files]

**Output Format:** [Markdown guidance with PowerShell command examples and generated Office files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates .docx or .xlsx outputs from user-specified source files or directories; existing output files may be overwritten.]

## Skill Version(s):

1.0.0 (source: server release evidence and skill metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
