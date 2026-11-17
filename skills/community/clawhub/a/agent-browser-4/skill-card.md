## Description:

Browser automation CLI for AI agents that need to interact with websites by navigating pages, filling forms, clicking buttons, taking screenshots, extracting data, testing web apps, or automating browser tasks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[justinpoulido](https://clawhub.ai/user/justinpoulido)

### License/Terms of Use:


## Use Case:

Developers and agents use this skill to automate browser workflows, including navigation, form submission, authenticated session reuse, screenshots, data extraction, web app testing, and visual debugging.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can invoke a powerful browser automation tool through an unpinned npm package.

Mitigation: Use a pinned, reviewed agent-browser version before execution.

Risk: Authenticated browser state, screenshots, videos, profiles, and traces can contain sensitive account data.

Mitigation: Store these artifacts outside shared or version-controlled locations with restrictive permissions, avoid real credentials in examples, and clear sessions after use.

Risk: Saved sessions may extend access to sensitive accounts beyond the immediate task.

Mitigation: Use saved sessions only when explicitly needed, prefer short-lived sessions for sensitive accounts, and remove stale session files.

## Reference(s):

- [Command Reference](references/commands.md)
- [Snapshot and Refs](references/snapshot-refs.md)
- [Session Management](references/session-management.md)
- [Authentication Patterns](references/authentication.md)
- [Video Recording](references/video-recording.md)
- [Profiling](references/profiling.md)
- [Proxy Support](references/proxy-support.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with bash commands, JSON examples, and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce browser artifacts such as screenshots, PDFs, videos, traces, extracted text, JSON snapshots, and saved session state when commands are executed.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
