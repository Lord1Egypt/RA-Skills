## Description:

Browser automation CLI for AI agents. Use when the user needs to interact with websites, including navigating pages, filling forms, clicking buttons, taking screenshots, extracting data, testing web apps, or automating any browser task.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shahaamirbader](https://clawhub.ai/user/shahaamirbader)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to control a browser for navigation, form interaction, data extraction, screenshots, PDFs, authenticated sessions, and web application testing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad live-browser control can navigate, click, submit forms, and extract page content with weak default scoping.

Mitigation: Review planned actions before execution and enable content boundaries, a domain allowlist, and a restrictive action policy for agent use.

Risk: Authentication state, screenshots, HARs, traces, PDFs, and recordings can contain sensitive data.

Mitigation: Use dedicated browser profiles and test accounts, encrypt saved state with AGENT_BROWSER_ENCRYPTION_KEY when available, and delete captured artifacts when no longer needed.

Risk: Installing or invoking latest executable packages can run unreviewed browser-control code.

Mitigation: Prefer a pinned, reviewed local agent-browser binary instead of npx/latest installs.

Risk: Attaching to an everyday Chrome session can expose personal cookies and logged-in accounts.

Mitigation: Avoid auto-connecting to the user's daily browser; use isolated sessions or profiles for automation work.

## Reference(s):

- [Authentication Patterns](references/authentication.md)
- [Command Reference](references/commands.md)
- [Profiling](references/profiling.md)
- [Proxy Support](references/proxy-support.md)
- [Session Management](references/session-management.md)
- [Snapshot and Refs](references/snapshot-refs.md)
- [Video Recording](references/video-recording.md)
- [Authenticated Session Template](templates/authenticated-session.sh)
- [Capture Workflow Template](templates/capture-workflow.sh)
- [Form Automation Template](templates/form-automation.sh)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands, code snippets, and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose or run browser automation commands and may produce captured files such as screenshots, PDFs, HARs, traces, recordings, and saved session state.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
