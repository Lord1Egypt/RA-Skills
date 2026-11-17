## Description:

Browser automation CLI for AI agents that need to navigate websites, fill forms, click buttons, take screenshots, extract data, test web apps, log in to sites, or automate browser tasks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thanhde91](https://clawhub.ai/user/thanhde91)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, QA engineers, and automation agents use this skill to drive Chrome or Chromium from the command line for web interaction, data extraction, authenticated browsing, capture, and web application testing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad browser automation authority can navigate, click, submit forms, download files, and mutate web state.

Mitigation: Use isolated test accounts and browser profiles, enable domain allowlists, and apply an action policy that limits commands to the minimum needed workflow.

Risk: Authentication workflows can expose cookies, localStorage, saved sessions, or credential-bearing state files.

Mitigation: Avoid importing a normal personal browser session, encrypt saved state with AGENT_BROWSER_ENCRYPTION_KEY, add state files to .gitignore, and delete auth artifacts when the task is complete.

Risk: Screenshots, PDFs, HAR files, recordings, traces, and downloaded content may contain sensitive information from authenticated pages.

Mitigation: Store captures in controlled locations, review and scrub outputs before sharing, and avoid publishing artifacts collected from authenticated or private pages.

Risk: Proxy guidance and web automation can be misused to bypass rate limits, bans, or site access controls.

Mitigation: Use proxies only for authorized testing or compliant operational needs, and do not use this skill to evade a site's policies or restrictions.

Risk: The executable browser automation tool is installed or upgraded outside the skill artifact.

Mitigation: Pin the executable version, review updates before upgrading, and run automation in a constrained environment appropriate for credential-handling tools.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thanhde91/skills/agent-browser-7)
- [Authentication Patterns](references/authentication.md)
- [Command Reference](references/commands.md)
- [Profiling](references/profiling.md)
- [Proxy Support](references/proxy-support.md)
- [Session Management](references/session-management.md)
- [Snapshot References](references/snapshot-refs.md)
- [Video Recording](references/video-recording.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands, code snippets, and configuration examples.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Agent-browser commands may produce browser screenshots, PDFs, HAR files, recordings, downloads, auth state files, and profiling traces when requested.]

## Skill Version(s):

0.1.0 (source: evidence.release.version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
