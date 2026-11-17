## Description:

A fast Rust-based headless browser automation CLI with Node.js fallback that enables AI agents to navigate, click, type, and snapshot pages via structured commands.

This skill is ready for commercial/non-commercial use.

## Publisher:

[keyserkazi1](https://clawhub.ai/user/keyserkazi1)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to automate browser interactions, extract page data, fill forms, and test web UIs through structured shell commands.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill recommends a mutable global install of the external agent-browser npm package.

Mitigation: Use a pinned, reviewed package version in a sandbox or container and avoid privileged global installs.

Risk: Browser automation can persist reusable login or session state and generate sensitive screenshots, PDFs, videos, or traces.

Mitigation: Avoid passing real passwords on the command line, protect generated artifacts, and delete auth state or recordings when no longer needed.

## Reference(s):

- [Agent Browser skill page](https://clawhub.ai/keyserkazi1/skills/agent-browser100)
- [Publisher profile](https://clawhub.ai/user/keyserkazi1)
- [agent-browser upstream CLI](https://github.com/vercel-labs/agent-browser)
- [Agent Browser skill issues](https://github.com/TheSethRose/Agent-Browser-CLI)

## Skill Output:

**Output Type(s):** [Shell commands, Markdown, Code, Configuration instructions, Guidance]

**Output Format:** [Markdown with inline bash code blocks and optional JSON command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires node and npm; browser artifacts such as auth state, screenshots, PDFs, videos, and traces may contain sensitive data.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
