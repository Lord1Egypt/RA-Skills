## Description:

Diagnose and fix gateway token mismatches causing 401 errors. Align tokens across config, service, and CLI surfaces.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dalomeve](https://clawhub.ai/user/dalomeve)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to diagnose OpenClaw gateway 401 errors and align gateway token values across configuration, service startup, and CLI environments.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Token audit commands can expose full gateway tokens in terminal output, logs, screenshots, transcripts, CI output, or support sessions.

Mitigation: Compare token values without printing them, redact any displayed token values, and avoid running the snippets as written in shared or recorded environments.

Risk: Token alignment steps can persist gateway tokens in startup scripts or exposed files.

Mitigation: Store tokens only in intended protected configuration locations, avoid saving tokens in startup scripts when possible, and rotate any token that was printed or saved somewhere exposed.

## Reference(s):

- [Privacy Checklist](references/privacy-checklist.md)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration]

**Output Format:** [Markdown with inline PowerShell code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes token-audit, alignment, and verification steps for OpenClaw gateway authentication.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
