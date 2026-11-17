## Description:

Accesses or controls a live local Chrome browser through Chrome DevTools MCP for opening pages, extracting rendered content, interacting with DOM elements, taking snapshots, and collecting website data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mallocfeng](https://clawhub.ai/user/mallocfeng)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use Chrome MCP Tools to inspect live, rendered web pages, including JavaScript-heavy or authenticated browser sessions, and return concise extracted content or summaries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can attach to a local Chrome session and read pages the user is logged into.

Mitigation: Use a separate browser profile for sensitive accounts and install only when browser-session access is acceptable.

Risk: The skill may automatically install or upgrade a global npm package before use.

Mitigation: Review the npm package source and resolved version before installation, and avoid automatic global upgrades where possible.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mallocfeng/skills/chromedev)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown or plain text with concise extracted page content, summaries, status messages, and occasional inline shell commands.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Final extracted answers are buffered and delivered as one complete response; blocked pages report visible content and the blocking condition.]

## Skill Version(s):

1.0.6 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
