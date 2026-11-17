## Description:

Scan code (Python, JavaScript/TypeScript, Java, C#, C/C++) for security vulnerabilities with the open-source Frame CLI or its MCP server, triage the findings, generate and verify fixes, and re-scan.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sandeep85das](https://clawhub.ai/user/sandeep85das)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to scan code they are authorized to review, triage security findings, and generate, inspect, verify, and re-scan proposed fixes. It asks for approval before sending code to an AI endpoint or changing files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The MCP setup command is not pinned to a package version.

Mitigation: Pin and review package versions before installation.

Risk: The optional AI layer may send repository code to an endpoint.

Mitigation: Approve and verify the endpoint before enabling AI features or sharing code.

Risk: Proposed fixes may introduce incorrect changes or affect existing files.

Mitigation: Review the proposed diff and keep a backup before applying changes.

Risk: A clean scan does not establish that code is secure.

Mitigation: Treat scan results as one input to security review and continue reviewing the code.

## Reference(s):

- [Frame project](https://github.com/lambdasec/frame)
- [Findings triage checklist](artifact/references/triage-checklist.md)

## Skill Output:

**Output Type(s):** [Analysis, Text, Markdown, JSON, Shell commands, Code]

**Output Format:** [Markdown summaries, JSON findings, shell commands, and proposed unified diffs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Finding details and proposed fixes depend on the scanned code and selected scan options.]

## Skill Version(s):

1.0.1 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
