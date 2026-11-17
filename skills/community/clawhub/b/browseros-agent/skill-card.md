## Description:

BrowserOS CLI helps an agent control a real Chromium browser for website interaction, including navigation, clicking, form filling, screenshots, tab management, bookmarks, and history.

This skill is ready for commercial/non-commercial use.

## Publisher:

[browseros-ai](https://clawhub.ai/user/browseros-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill when a task requires real browser interaction beyond static page fetching, such as clicking elements, filling forms, navigating multi-step workflows, taking screenshots, testing web apps, or managing tabs, bookmarks, and history.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill allows an agent to control a real browser and make persistent changes such as submitting forms, uploading or downloading files, changing bookmarks or history, and closing tabs or windows.

Mitigation: Use an isolated browser profile where possible and require explicit approval before form submission, uploads or downloads, history or bookmark changes, and closing existing tabs or windows.

Risk: The installation path can use an unpinned browser-control CLI version.

Mitigation: Prefer a pinned, reviewed BrowserOS CLI version and install only from a trusted source.

## Reference(s):

- [BrowserOS CLI Command Reference](references/cli-commands.md)
- [BrowserOS](https://browseros.com)
- [BrowserOS CLI Source](https://github.com/browseros-ai/BrowserOS/tree/main/packages/browseros-agent/apps/cli)
- [BrowserOS MCP Setup Guide](https://docs.browseros.com/features/use-with-claude-code)
- [BrowserOS Skills Repository](https://github.com/browseros-ai/skills)
- [ClawHub Skill Page](https://clawhub.ai/browseros-ai/skills/browseros-agent)

## Skill Output:

**Output Type(s):** [Shell commands, Markdown, Code, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands and command references]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce browser state changes, screenshots, PDFs, downloads, bookmark/history changes, or tab/window changes when the agent executes BrowserOS CLI commands.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
