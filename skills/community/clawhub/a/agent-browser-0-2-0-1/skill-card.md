## Description:

A fast Rust-based headless browser automation CLI with Node.js fallback that enables AI agents to navigate, click, type, and snapshot pages via structured commands.

This skill is ready for commercial/non-commercial use.

## Publisher:

[liu-zaa](https://clawhub.ai/user/liu-zaa)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and AI agent operators use this skill to automate browser navigation, interaction, data extraction, UI testing, screenshots, recordings, and authenticated session workflows through the agent-browser CLI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Mutable package installs can change the executed browser automation code over time.

Mitigation: Prefer a pinned package version or audited commit before enabling the skill in managed environments.

Risk: Saved browser state, recordings, cookies, and localStorage exports can expose authenticated session data.

Mitigation: Use test or low-privilege accounts and protect generated state files and recordings like credentials.

Risk: Browser automation can operate inside authenticated sessions and perform unintended web actions.

Mitigation: Run without admin privileges and enable the skill only for trusted workflows and trusted upstream packages.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/liu-zaa/skills/agent-browser-0-2-0-1)
- [Agent Browser CLI repository](https://github.com/vercel-labs/agent-browser)
- [Agent Browser Skill issue repository](https://github.com/TheSethRose/Agent-Browser-CLI)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, JSON, Files]

**Output Format:** [Markdown guidance with bash command examples; CLI operations may return text, JSON, screenshots, PDFs, trace archives, or video files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires node and npm; browser automation can use saved cookies, localStorage, recordings, and other state files.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact metadata version 0.2.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
