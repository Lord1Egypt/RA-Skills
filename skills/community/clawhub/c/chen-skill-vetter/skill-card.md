## Description:

Security-first skill vetting for AI agents. Use before installing any skill from ClawdHub, GitHub, or other sources. Checks for red flags, permission scope, and suspicious patterns.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cs995279497-byte](https://clawhub.ai/user/cs995279497-byte)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to review third-party or unknown agent skills before installation by checking source trust, permissions, red flags, and risk level.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Network access may be needed when inspecting remote GitHub repositories.

Mitigation: Allow network access only when intentionally reviewing a remote repository and restrict review activity to expected repository hosts.

Risk: Reviewing an untrusted target skill in a broad workspace can expose private or sensitive files.

Mitigation: Inspect target skills in a controlled workspace and avoid granting access to credentials or unrelated home-directory files.

Risk: The vetting report is advisory and may miss hidden or context-dependent unsafe behavior.

Mitigation: Pair the checklist with full file review, scanner results, and human approval for high-risk permissions or credential access.

## Reference(s):


## Skill Output:

**Output Type(s):** [guidance, markdown, shell commands]

**Output Format:** [Markdown vetting report with optional shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [None]

## Skill Version(s):

1.0.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
