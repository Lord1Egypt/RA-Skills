## Description:

Browser automation CLI for AI agents that helps navigate pages, fill forms, click buttons, take screenshots, extract data, test web apps, and automate browser tasks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[winchester-yi](https://clawhub.ai/user/winchester-yi)

### License/Terms of Use:


## Use Case:

Developers and AI agents use this skill to drive browser workflows such as navigation, form submission, authenticated sessions, content capture, visual evidence collection, and web app testing from shell commands.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill enables broad browser automation, including navigation, clicks, form submission, downloads, JavaScript evaluation, local file access, and connection to existing browser sessions.

Mitigation: Supervise runs and use domain allowlists, action policies, fresh snapshots after page changes, and explicit review before submitting forms or performing destructive actions.

Risk: Authenticated sessions, saved state files, cookies, recordings, traces, proxy credentials, and screenshots can expose sensitive information.

Mitigation: Prefer the encrypted auth vault, keep state files and artifacts out of source control, clear or delete credentials after use, and treat generated browser artifacts like secrets.

Risk: Proxy guidance and scraping workflows could be misused to bypass rate limits, bans, or site policies.

Mitigation: Use proxies only for legitimate testing or approved network access, follow site terms and rate limits, and avoid automation intended to evade restrictions.

Risk: The authoritative scan verdict is suspicious because the skill grants powerful browser, credential, session, proxy, and persistence capabilities with under-scoped safety guidance.

Mitigation: Review the skill and its operational policy before deployment, restrict trusted domains and actions, and monitor generated files and browser state during use.

## Reference(s):

- [Agent Browser ClawHub Page](https://clawhub.ai/winchester-yi/skills/agent-browser-vercel)
- [Command Reference](references/commands.md)
- [Snapshot and Refs](references/snapshot-refs.md)
- [Session Management](references/session-management.md)
- [Authentication Patterns](references/authentication.md)
- [Video Recording](references/video-recording.md)
- [Profiling](references/profiling.md)
- [Proxy Support](references/proxy-support.md)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, Markdown, Code, Guidance]

**Output Format:** [Markdown guidance with inline bash commands, JSON configuration examples, and reusable shell script templates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce browser state files, screenshots, PDFs, WebM recordings, trace files, and extracted text when the recommended commands are executed.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
