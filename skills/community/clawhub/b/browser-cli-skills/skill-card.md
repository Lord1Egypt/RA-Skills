## Description:

Controls Chrome browsers from the terminal via the AIPex extension for tab management, element interaction, form filling, screenshots, and content downloads without an MCP client.

This skill is ready for commercial/non-commercial use.

## Publisher:

[buttercannfly](https://clawhub.ai/user/buttercannfly)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and automation engineers use this skill to drive Chrome browser workflows from shell commands, including tab management, page inspection, element interaction, screenshots, content download, and human intervention requests.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Powerful browser automation can act in logged-in browser sessions or expose sensitive page content through screenshots.

Mitigation: Use a low-risk browser profile, supervise actions in sensitive sessions, and avoid sending screenshots to an LLM when pages contain private data.

Risk: Global latest installs and self-updates can change behavior unexpectedly.

Mitigation: Prefer pinned or reviewed browser-cli versions before installation or update.

Risk: Skill-script execution may run external skill code without enough safety boundaries.

Mitigation: Review skill scripts and run them in a constrained environment before deployment.

## Reference(s):

- [browser-cli homepage](https://github.com/AIPexStudio/browser-cli)

## Skill Output:

**Output Type(s):** [shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js 18 or newer, npm, and an AIPex Chrome extension connection.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
