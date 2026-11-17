## Description:

Codepal is a Bash devtools logger for recording, searching, summarizing, and exporting developer notes about code review, linting, code generation, diffs, fixes, and repository understanding.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xueyetianya](https://clawhub.ai/user/xueyetianya)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use Codepal to keep a local activity trail of code review findings, lint notes, generated snippet descriptions, diffs, fixes, and repo-understanding notes, then search or export those records.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Developer text entered into Codepal can include secrets, proprietary source, customer data, or sensitive vulnerability notes and is retained locally under ~/.local/share/codepal.

Mitigation: Avoid entering sensitive material unless local retention and later search or export are acceptable; review and remove local logs before sharing exports or workstations.

Risk: The release is marketed as AI code analysis, while the security evidence says the script mainly saves and exports entered developer text.

Mitigation: Treat Codepal as a local logging and export utility, and use separate trusted analysis, review, or scanning tools for code-quality and security conclusions.

## Reference(s):

- [Codepal on ClawHub](https://clawhub.ai/xueyetianya/skills/codepal)
- [BytesAgain homepage](https://bytesagain.com)

## Skill Output:

**Output Type(s):** [text, shell commands, files]

**Output Format:** [Plain text command output with local log and export files in text, JSON, or CSV formats]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes timestamped records under ~/.local/share/codepal and can export accumulated records.]

## Skill Version(s):

2.0.1 (source: server release metadata; artifact frontmatter and script report 2.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
