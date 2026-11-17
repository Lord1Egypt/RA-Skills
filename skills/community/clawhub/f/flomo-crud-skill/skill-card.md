## Description:

Query, insert, edit, and delete flomo memos through the flomo Web UI using Chrome MCP tools (no official API required).

This skill is ready for commercial/non-commercial use.

## Publisher:

[undertone0809](https://clawhub.ai/user/undertone0809)

### License/Terms of Use:


## Use Case:

Developers and agent users use this skill to search, create, replace, and delete live flomo memos through a logged-in Chrome session when an official API is not available or not desired.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The recommended setup can automatically run an unpinned browser bridge package in a logged-in Chrome environment.

Mitigation: Review the Chrome MCP setup before installing, prefer a pinned and reviewed version of mcp-chrome-bridge, and avoid automatic first-time npx execution when possible.

Risk: The skill operates on live flomo memos, including edits and destructive deletion.

Mitigation: Check the displayed memo_id, timestamp, and snippet before writes, require candidate confirmation for text-search edits, and require explicit second confirmation before deletion.

Risk: Browser UI changes or ambiguous page state can cause automation to target the wrong control.

Mitigation: Prefer fresh structured page refs, lock write targets by memo_id, and stop with a recoverable failure when controls or dialog state cannot be located reliably.

## Reference(s):

- [Workflow details](references/workflows.md)
- [UI locator strategy and fallback policy](references/ui-locators.md)
- [Safety and logging policy](references/safety.md)
- [Validation checklist](references/test-checklist.md)
- [flomo Web](https://v.flomoapp.com/mine)
- [hangwin/mcp-chrome](https://github.com/hangwin/mcp-chrome)
- [ClawHub skill page](https://clawhub.ai/undertone0809/skills/flomo-crud-skill)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown and concise text with optional inline shell commands or configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns memo candidates and action results; does not persist memo body text by default.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
