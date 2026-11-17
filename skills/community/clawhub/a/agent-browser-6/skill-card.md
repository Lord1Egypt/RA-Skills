## Description:

Browser automation CLI for AI agents. Use when the user needs to interact with websites, including navigating pages, filling forms, clicking buttons, taking screenshots, extracting data, testing web apps, or automating any browser task.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chulla-ceja](https://clawhub.ai/user/chulla-ceja)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to drive browser workflows for website interaction, form automation, data extraction, authenticated sessions, screenshots, PDFs, and web app testing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can reuse logged-in browser sessions and persist authentication state, which can expose cookies, local storage, or session tokens.

Mitigation: Use dedicated browser profiles, encrypt saved state with AGENT_BROWSER_ENCRYPTION_KEY, keep state files out of version control, and delete them when no longer needed.

Risk: The skill can perform high-privilege browser automation, run page scripts, and navigate without default restrictions.

Mitigation: Enable domain allowlists, content boundaries, and an action policy before using it on sensitive sites or with untrusted page content.

Risk: The skill can execute unpinned agent-browser tooling.

Mitigation: Install only from trusted package sources and prefer a pinned, verified binary for repeatable or sensitive workflows.

Risk: Proxy and recording workflows can capture or route sensitive browsing activity.

Mitigation: Avoid recording or profiling sensitive login and account workflows, and do not use proxy rotation to bypass site rules.

## Reference(s):

- [Agent Browser ClawHub release](https://clawhub.ai/chulla-ceja/skills/agent-browser-6)
- [Authentication Patterns](references/authentication.md)
- [Command Reference](references/commands.md)
- [Profiling](references/profiling.md)
- [Proxy Support](references/proxy-support.md)
- [Session Management](references/session-management.md)
- [Snapshot and Refs](references/snapshot-refs.md)
- [Video Recording](references/video-recording.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May also point to generated browser artifacts such as screenshots, PDFs, recordings, traces, downloaded files, saved state files, and profile directories.]

## Skill Version(s):

0.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
