## Description:

Know the file you are editing is the file you think it is: verify integrity before you act.

This skill is ready for commercial/non-commercial use.

## Publisher:

[leegitw](https://clawhub.ai/user/leegitw)

### License/Terms of Use:

MIT

## Use Case:

Developers and engineers use this skill to compute and verify SHA-256 file hashes, tag file-change severity, and create context packets before editing or review workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can hash any file path explicitly provided by the user, including sensitive files.

Mitigation: Use deliberate file paths and avoid broad globs when secrets or credentials may be present.

Risk: Using --include-content stores file contents in unencrypted context packets on disk.

Mitigation: Do not use --include-content with secrets, add output/context-packets/ to .gitignore, restrict permissions, and delete packets when no longer needed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/leegitw/skills/context-verifier)
- [Project homepage](https://github.com/live-neon/skills/tree/main/agentic/context-verifier)

## Skill Output:

**Output Type(s):** [Text, JSON, Guidance]

**Output Format:** [Plain text status output and JSON context packet files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write unencrypted context packet JSON under output/context-packets/ when packet creation is requested.]

## Skill Version(s):

1.5.1 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
