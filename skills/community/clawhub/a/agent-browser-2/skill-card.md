## Description:

Automates browser interactions for web testing, form filling, screenshots, and data extraction.

This skill is ready for commercial/non-commercial use.

## Publisher:

[murphykobe](https://clawhub.ai/user/murphykobe)

### License/Terms of Use:


## Use Case:

Developers and automation engineers use this skill to navigate websites, interact with pages, fill forms, capture screenshots or PDFs, record browser sessions, and extract page information through agent-browser commands.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Saved browser state can contain cookies, tokens, and other authentication material.

Mitigation: Use test accounts where possible, save state only when necessary, keep state files private with restrictive permissions, and delete them after use.

Risk: Browser recordings, screenshots, PDFs, and extracted text can capture private data or login flows.

Mitigation: Avoid recording credentials or sensitive pages, review generated artifacts before sharing, and remove sensitive files after the workflow completes.

Risk: Proxy URLs and browser credentials can expose secrets through shell history or logs.

Mitigation: Provide credentials through environment variables or a secure secret store, and keep proxy credentials out of command history and logs.

Risk: Automation against logged-in or production sites can perform unintended actions.

Mitigation: Review workflows before execution, prefer test environments, confirm element refs after page changes, and use isolated browser sessions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/murphykobe/skills/agent-browser-2)
- [Snapshot + Refs Workflow](artifact/references/snapshot-refs.md)
- [Session Management](artifact/references/session-management.md)
- [Authentication Patterns](artifact/references/authentication.md)
- [Video Recording](artifact/references/video-recording.md)
- [Proxy Support](artifact/references/proxy-support.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown guidance with inline shell commands and optional JSON command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce screenshots, PDFs, WebM recordings, browser state files, and extracted page text through agent-browser commands.]

## Skill Version(s):

0.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
