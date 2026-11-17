## Description:

Browser automation CLI for AI agents that connects to a running Google Chrome instance over CDP for website navigation, form interaction, screenshots, data extraction, and other browser tasks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[joustonhuang](https://clawhub.ai/user/joustonhuang)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to control an existing Chrome session from an agent, including authenticated browsing, page inspection, form filling, screenshots, and browser workflow automation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad Chrome CDP control can expose logged-in sessions, cookies, local storage, and page content to any process that can reach the debugging endpoint.

Mitigation: Use a trusted isolated environment, a dedicated Chrome profile, a low-privilege OS account, domain and action restrictions, and close the debugging session when work is complete.

Risk: The setup flow uses mutable install commands and can require privileged system changes.

Mitigation: Pin and inspect the setup script and npm package before running them, and avoid sudo unless the exact commands have been reviewed.

Risk: Saved auth state, recordings, screenshots, PDFs, and traces may contain secrets or private data.

Mitigation: Treat generated browser artifacts as secrets, keep them out of source control, encrypt or restrict access where possible, and delete them when no longer needed.

Risk: Web page content can contain prompt-injection text that attempts to steer the agent into unsafe browser actions.

Mitigation: Enable content boundaries, restrict allowed domains, gate destructive actions with policy, and review high-impact actions before execution.

## Reference(s):

- [Chrome for OpenClaw Homepage](https://github.com/joustonhuang/chrome_for_openclaw)
- [Chrome CDP for OpenClaw on ClawHub](https://clawhub.ai/joustonhuang/skills/chrome-for-openclaw)
- [Command Reference](references/commands.md)
- [Authentication Patterns](references/authentication.md)
- [Session Management](references/session-management.md)
- [Snapshot and Refs](references/snapshot-refs.md)
- [Video Recording](references/video-recording.md)
- [Profiling](references/profiling.md)
- [Proxy Support](references/proxy-support.md)
- [agent-browser CLI](https://github.com/vercel-labs/agent-browser)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline shell commands and command references]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include generated browser artifacts such as screenshots, PDFs, videos, traces, and auth-state files when agent-browser commands are used.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
