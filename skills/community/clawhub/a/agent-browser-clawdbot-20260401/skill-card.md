## Description:

Headless browser automation CLI optimized for AI agents with accessibility tree snapshots and ref-based element selection.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dahai520520520](https://clawhub.ai/user/dahai520520520)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and AI agents use this skill to automate browser navigation, interaction, state inspection, and extraction workflows through the agent-browser CLI. It is suited for deterministic multi-step browser tasks, complex SPAs, session isolation, and command-oriented testing or data collection workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Saved browser state can include cookies, localStorage, and authentication material.

Mitigation: Use isolated environments and test accounts where possible; do not commit or share saved state files, and delete them when no longer needed.

Risk: A broad unpinned global npm installation can install unexpected package versions or alter the host environment.

Mitigation: Review and pin the npm package version before installation, and avoid elevated privileges unless the host changes are understood.

## Reference(s):

- [agent-browser GitHub repository](https://github.com/vercel-labs/agent-browser)
- [ClawHub skill page](https://clawhub.ai/dahai520520520/skills/agent-browser-clawdbot-20260401)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, Guidance, JSON]

**Output Format:** [Markdown with bash and JSON code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May guide agents to create browser artifacts such as screenshots, PDFs, cookies, localStorage, and saved auth state when the generated commands are executed.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
