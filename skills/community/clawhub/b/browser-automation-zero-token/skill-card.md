## Description:

Build and run low-code browser automation workflows with agent-browser CLI and reusable skills for repeatable web tasks such as sign-ins, form fills, dashboard checks, fixed click flows, and saved-state routines.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cnxufei-tech](https://clawhub.ai/user/cnxufei-tech)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and automation builders use this skill to convert stable browser workflows into repeatable agent-browser command sequences, reusable site-specific skill instructions, debugging checklists, and saved-state recurring routines.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Saved browser session state can preserve reusable logged-in access in a local auth file.

Mitigation: Treat saved state files like passwords: keep them outside project folders, restrict permissions, never commit or share them, use separate files per site or account, and revoke or delete sessions when no longer needed.

Risk: Global CLI installation can introduce unpinned dependency risk.

Mitigation: Pin and verify agent-browser where possible before installing global dependencies.

Risk: Browser automation may act on accounts, sites, or workflows where automation is not authorized.

Mitigation: Confirm user authorization, site permission, and credentials before running automated browser interactions.

## Reference(s):

- [Source Notes](references/source-notes.md)
- [ClawHub Skill Page](https://clawhub.ai/cnxufei-tech/skills/browser-automation-zero-token)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell command blocks and concise workflow guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include reusable command sequences, site-specific skill drafts, auth-state routines, and debugging checklists.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
