## Description:

AI desktop agent that lets an OpenClaw agent control Windows and macOS apps through local desktop and browser automation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sieyer](https://clawhub.ai/user/sieyer)

### License/Terms of Use:


## Use Case:

Developers and agent users use this skill to automate user-requested desktop, browser, form-filling, visual verification, and cross-app workflows when a direct API, CLI, or file operation is not available.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill enables a local service to see and operate the user's desktop and browser.

Mitigation: Install only when desktop-control access is acceptable, use a local provider such as Ollama for private screens, and require explicit user confirmation before sensitive app use.

Risk: The reviewed artifact may depend on mutable remote code and agent-started local services.

Mitigation: Prefer a version pinned to a reviewed commit with locked dependencies, and require confirmation before starting or using the service.

Risk: Chrome remote debugging can expose browser control if enabled unnecessarily.

Mitigation: Keep Chrome remote debugging disabled unless it is intentionally needed for the current task.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/sieyer/skills/clawd-cursor-0-6-0)
- [Publisher profile](https://clawhub.ai/user/sieyer)
- [Clawd Cursor homepage](https://clawdcursor.com)
- [Skill-declared source link](https://github.com/AmrDab/clawd-cursor)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, API calls, Code]

**Output Format:** [Markdown with inline shell, PowerShell, JavaScript, and REST examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May issue local REST requests to a desktop-control service and CDP browser automation commands when the service is running.]

## Skill Version(s):

0.6.0 (source: SKILL.md frontmatter; ClawHub release version 1.0.0 from server metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
