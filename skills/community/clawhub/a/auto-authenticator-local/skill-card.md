## Description:

Auto Authenticator Local helps authorized users store TOTP seeds in system credential stores, generate 6-digit codes on explicit request, wire approved login flows, and handle local secrets safely.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lucaszh7](https://clawhub.ai/user/lucaszh7)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and authorized operators use this skill for local-only TOTP storage and explicit on-demand code generation for accounts they own or are authorized to manage.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: TOTP seeds entered directly on the command line can remain in shell history or process metadata.

Mitigation: Avoid entering real TOTP seeds in long-lived shell history; prefer a reviewed secure-entry path and redact account labels when needed.

Risk: Installing through curl piped to bash or an unpinned source can execute installer changes before review.

Mitigation: Review the installer first or install from a pinned, inspectable release.

Risk: A custom OPENCLAW_SKILL_DIR can point installation at a directory containing valuable local files.

Mitigation: Use a dedicated skill directory and do not set OPENCLAW_SKILL_DIR to a location with valuable files.

Risk: TOTP code generation can create access risk if used outside authorized account workflows.

Mitigation: Use the skill only for accounts the user owns or is explicitly authorized to manage, and require an explicit alias for each code request.

## Reference(s):

- [Security notes for local TOTP workflows](artifact/references/security.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and concise command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Scoped to one explicit alias per code-generation request.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact/manifest.yaml)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
