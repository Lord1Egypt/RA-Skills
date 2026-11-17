## Description:

ClawdCursor is an OS-level desktop automation tool server with 42 tools for controlling applications on Windows, macOS, and Linux through REST or MCP.

This skill is ready for commercial/non-commercial use.

## Publisher:

[amrdab](https://clawhub.ai/user/amrdab)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill when native APIs, CLIs, direct file edits, or browser automation are unavailable and a task requires local desktop interaction across applications.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release is a desktop automation tool that can read screen content, use the clipboard, interact with browser tabs, and control local applications.

Mitigation: Review permissions before installing, keep the service bound to localhost, and require user confirmation for sends, deletes, purchases, or other irreversible actions.

Risk: The install flow uses an unpinned global executable and includes commands that accept consent and start the service.

Mitigation: Prefer a pinned package version and avoid automatic consent or startup until the executable, permissions, and local token behavior have been reviewed.

## Reference(s):

- [ClawdCursor Skill Page](https://clawhub.ai/amrdab/skills/clawdcursor)
- [ClawdCursor Homepage](https://clawdcursor.com)
- [ClawdCursor Source](https://github.com/AmrDab/clawdcursor)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, API calls]

**Output Format:** [Markdown with command, JSON, and HTTP examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guidance is oriented around local desktop automation, REST or MCP tool use, and verification after sensitive actions.]

## Skill Version(s):

0.7.5 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
