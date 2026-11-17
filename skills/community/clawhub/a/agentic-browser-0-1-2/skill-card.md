## Description:

Agentic Browser provides browser automation for AI agents via inference.sh, enabling navigation, element interaction with @e references, screenshots, video recording, file uploads, and JavaScript execution.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xyny89](https://clawhub.ai/user/xyny89)

### License/Terms of Use:


## Use Case:

Developers and agents use this skill to automate browser workflows such as web navigation, data extraction, form filling, browser testing, screenshots, video capture, authenticated sessions, proxy-based checks, and JavaScript-driven page inspection.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill relies on a hosted browser service that may handle pages, credentials, files, screenshots, videos, cookies, and proxy settings.

Mitigation: Use only with trusted targets and providers, prefer test or least-privilege accounts, avoid sensitive local file uploads, and limit the data sent through browser sessions.

Risk: The documented installer pipes a remote script to the shell.

Mitigation: Inspect or verify the installer independently before execution, or use an installation path that allows review before running code.

Risk: Screenshots and video recordings can capture credentials, admin screens, private data, or regulated content.

Mitigation: Disable recording for login and sensitive workflows, redact outputs before sharing, and keep recordings only as long as needed.

Risk: Persistent sessions can retain cookies and authenticated browser state.

Mitigation: Close sessions promptly, separate tasks into distinct sessions, and clean up sessions on errors or script exit.

## Reference(s):

- [Agentic Browser skill page](https://clawhub.ai/xyny89/skills/agentic-browser-0-1-2)
- [Command Reference](references/commands.md)
- [Snapshot and Refs](references/snapshot-refs.md)
- [Session Management](references/session-management.md)
- [Authentication Patterns](references/authentication.md)
- [Video Recording](references/video-recording.md)
- [Proxy Support](references/proxy-support.md)
- [inference.sh Sessions](https://inference.sh/docs/extend/sessions)
- [inference.sh Multi-function Apps](https://inference.sh/docs/extend/multi-function-apps)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with shell command examples and JSON inputs.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose browser sessions, screenshots, videos, extracted page text, file upload steps, proxy settings, and JavaScript snippets.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
