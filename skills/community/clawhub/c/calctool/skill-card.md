## Description:

CalcTool provides terminal commands for recording, searching, and displaying calculation-related entries in local plaintext logs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ckchzh](https://clawhub.ai/user/ckchzh)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, analysts, and external users use this skill to record calculation, conversion, comparison, analysis, status, and report entries from a shell workflow. Server security evidence indicates the artifact primarily stores, searches, and displays user-entered text in persistent local logs rather than performing live calculation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: User-entered command values may be persisted locally in plaintext logs and later searched or displayed.

Mitigation: Avoid entering credentials, account numbers, financial details, confidential reports, or private business data unless local logging is intended and file permissions are hardened.

Risk: The artifact is advertised as a calculator, but server security evidence says it mainly stores, searches, and displays entered text.

Mitigation: Review behavior before installation and do not rely on it for independent calculation correctness without separate verification.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ckchzh/skills/calctool)
- [Publisher profile](https://clawhub.ai/user/ckchzh)
- [BytesAgain homepage](https://bytesagain.com)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and plain-text command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce or inspect local plaintext log files under ~/.local/share/calctool when installed and executed.]

## Skill Version(s):

2.0.1 (source: server release evidence; artifact frontmatter and script report 2.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
