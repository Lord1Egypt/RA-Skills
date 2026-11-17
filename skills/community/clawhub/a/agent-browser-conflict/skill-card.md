## Description:

A fast Rust-based headless browser automation CLI with Node.js fallback that enables AI agents to navigate, click, type, and snapshot pages via structured commands.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nuradil](https://clawhub.ai/user/nuradil)

### License/Terms of Use:


## Use Case:

Developers and AI agents use this skill to automate browser navigation, inspect page structure, interact with web UI elements, fill forms, capture screenshots or PDFs, and extract structured page data from command-line workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks users to install a mutable global browser automation CLI and optional browser dependencies.

Mitigation: Review installation steps before use, run in an isolated or disposable environment, pin and verify the agent-browser package version when possible, and avoid running --with-deps with elevated privileges unless the host changes are understood.

Risk: Saved browser state files such as auth.json can contain reusable authenticated session data.

Mitigation: Treat saved state files as credentials; do not commit, share, or reuse them across unrelated tasks, and delete them when finished.

## Reference(s):

- [Agent Browser skill page](https://clawhub.ai/nuradil/skills/agent-browser-conflict)
- [agent-browser CLI repository](https://github.com/vercel-labs/agent-browser)
- [Agent Browser skill issue repository](https://github.com/TheSethRose/Agent-Browser-CLI)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Text, JSON, Files]

**Output Format:** [Markdown guidance with inline bash commands; command output may include text, JSON, screenshots, PDFs, and recordings.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires node and npm; browser state files can persist authenticated sessions.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
