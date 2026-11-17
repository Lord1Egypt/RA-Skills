## Description:

Browser automation CLI for AI agents. Use when the user needs to interact with websites, including navigating pages, filling forms, clicking buttons, taking screenshots, extracting data, testing web apps, or automating any browser task.

This skill is ready for commercial/non-commercial use.

## Publisher:

[equalearning](https://clawhub.ai/user/equalearning)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to control Chrome or Chromium for web navigation, form automation, authenticated browsing, content extraction, screenshots, PDFs, video recording, profiling, and web app testing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can control browser sessions broadly, including navigation, clicks, JavaScript evaluation, downloads, clipboard access, and authenticated workflows.

Mitigation: Use a dedicated browser profile, enable domain allowlists, and configure an action policy that denies destructive actions unless explicitly allowed.

Risk: Saved state files and reused profiles can contain session tokens or other credentials.

Mitigation: Treat state files as credentials, keep them out of shared logs and repositories, delete them when no longer needed, and set AGENT_BROWSER_ENCRYPTION_KEY for encryption at rest.

Risk: Screenshots, PDFs, recordings, traces, and extracted page text can contain sensitive page content.

Mitigation: Store captures in controlled locations, avoid committing or sharing them by default, and review artifacts before exposing them outside the trusted environment.

Risk: Page-sourced output can influence an agent's next actions.

Mitigation: Enable content boundaries, limit output size, and review page-derived instructions before acting on them.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/equalearning/skills/agent-browser-5)
- [Command Reference](references/commands.md)
- [Snapshot and Refs](references/snapshot-refs.md)
- [Session Management](references/session-management.md)
- [Authentication Patterns](references/authentication.md)
- [Video Recording](references/video-recording.md)
- [Profiling](references/profiling.md)
- [Proxy Support](references/proxy-support.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files]

**Output Format:** [Markdown guidance with inline shell commands, configuration snippets, reusable shell templates, and browser-captured files such as screenshots, PDFs, videos, traces, profiles, and extracted page text.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce persistent browser state, authentication files, downloaded files, clipboard interactions, screenshots, PDFs, WebM recordings, and Chrome DevTools trace/profile JSON depending on the workflow.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
