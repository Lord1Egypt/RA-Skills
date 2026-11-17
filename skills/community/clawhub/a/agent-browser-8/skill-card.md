## Description:

Agent Browser guides AI agents in using the agent-browser CLI to navigate websites, interact with page elements, capture screenshots or PDFs, extract data, and test web apps.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hayasam](https://clawhub.ai/user/hayasam)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and AI-agent operators use this skill when an agent needs controlled browser automation for web interaction, data capture, authenticated workflows, or web app testing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill enables strong browser control, including navigation and element interaction.

Mitigation: Use a dedicated disposable browser profile and enable domain allowlists, content boundaries, output limits, and a restrictive action policy before use.

Risk: Browser state files and captured artifacts can contain session tokens, credentials, or sensitive page content.

Mitigation: Avoid normal Chrome profiles, treat saved state, screenshots, recordings, HARs, PDFs, and traces as sensitive, and encrypt or delete authentication state promptly.

Risk: Floating npx or latest installs can run an unpinned external CLI version.

Mitigation: Use a pinned, verified agent-browser version for deployments.

## Reference(s):

- [Authentication Patterns](references/authentication.md)
- [Command Reference](references/commands.md)
- [Profiling](references/profiling.md)
- [Proxy Support](references/proxy-support.md)
- [Session Management](references/session-management.md)
- [Snapshot and Refs](references/snapshot-refs.md)
- [Video Recording](references/video-recording.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and reusable shell script templates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May direct an agent to produce browser captures such as screenshots, PDFs, HAR files, traces, recordings, extracted text, and session state files.]

## Skill Version(s):

0.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
