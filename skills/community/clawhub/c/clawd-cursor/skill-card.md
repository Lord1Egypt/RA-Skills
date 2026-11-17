## Description:

AI desktop agent that lets an OpenClaw agent control visible Windows or macOS applications by opening apps, clicking, typing, navigating browsers, filling forms, and reading screens.

This skill is ready for commercial/non-commercial use.

## Publisher:

[amrdab](https://clawhub.ai/user/amrdab)

### License/Terms of Use:


## Use Case:

Developers and OpenClaw users use this skill when a task requires GUI-level interaction that direct filesystem, shell, API, or browser tools cannot complete. It is suited for desktop app workflows, browser form interaction, visual verification, and cross-application tasks under user-controlled safety approvals.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill enables broad desktop automation with access to visible screens and applications.

Mitigation: Run it only with explicit user intent, prefer a constrained user account or VM, and avoid sensitive apps such as email, banking, password managers, admin consoles, or private messages unless the user confirms the specific task.

Risk: The release asks users to install and run mutable remote code before using the local service.

Mitigation: Verify the upstream repository and package versions before installation, then run the documented doctor command before starting the service.

Risk: Screenshots and UI text may be sent to a configured cloud AI provider when local mode is not used.

Mitigation: Prefer Ollama or another local provider when possible, and confirm that cloud-provider routing matches the user's data-handling expectations before processing sensitive screens.

Risk: GUI automation can perform consequential actions such as sending messages, deleting data, or changing settings.

Mitigation: Use direct tools first, escalate only residual UI steps, and require user confirmation for sensitive or irreversible actions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/amrdab/skills/clawd-cursor)
- [Publisher profile](https://clawhub.ai/user/amrdab)
- [Clawd Cursor homepage](https://clawdcursor.com)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline code blocks, shell commands, and REST API examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include local API requests, polling steps, browser automation snippets, setup commands, and safety confirmation guidance.]

## Skill Version(s):

0.6.3 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
