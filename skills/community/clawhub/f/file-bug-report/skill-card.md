## Description:

Creates triage-ready OpenClaw GitHub issue drafts by collecting conservative diagnostics, comparing configuration and plugin state, searching similar issues, and preparing a reviewed bug report.

This skill is ready for commercial/non-commercial use.

## Publisher:

[100yenadmin](https://clawhub.ai/user/100yenadmin)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and support engineers use this skill to turn vague OpenClaw agent failures into privacy-conscious diagnostics, duplicate-search notes, and GitHub issue drafts for maintainer triage.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The diagnostics workflow can collect local OpenClaw state, configuration metadata, plugin information, and log excerpts that may contain sensitive local details.

Mitigation: Use the default conservative collection mode, write output to a private directory, inspect every generated file, and share only selected redacted excerpts.

Risk: Users may accidentally publish an entire diagnostics bundle or unreviewed logs to a public issue.

Mitigation: Keep the workflow draft-only until explicit user approval, do not attach the full bundle publicly, and paste only reviewed excerpts into the issue body.

Risk: Optional collection flags can include private config, temporary logs, or raw git details.

Mitigation: Enable those flags only after explaining the privacy risk and receiving explicit user approval.

Risk: Generated output written into a shared location may be readable by unintended local users.

Mitigation: Choose a private output directory before running diagnostics because the security guidance notes that the script does not force restrictive file permissions.

## Reference(s):

- [OpenClaw Bug Report ClawHub page](https://clawhub.ai/100yenadmin/skills/file-bug-report)
- [OpenClaw Agent Bug Issue Template](references/issue-template.md)
- [Similar Issue Search](references/similar-issue-search.md)
- [Conservative OpenClaw diagnostics collector](scripts/collect-openclaw-diagnostics.sh)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown issue drafts with inline shell commands and summarized diagnostics]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Draft-only public output until the user reviews selected excerpts and approves posting.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
