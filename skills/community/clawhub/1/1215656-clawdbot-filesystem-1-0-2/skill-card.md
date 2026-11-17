## Description:

Advanced filesystem operations - listing, searching, batch processing, and directory analysis for Clawdbot.

This skill is ready for commercial/non-commercial use.

## Publisher:

[1215656](https://clawhub.ai/user/1215656)

### License/Terms of Use:

MIT

## Use Case:

Developers and agent operators use this skill to list, search, copy, visualize, and analyze files and directories from a Clawdbot workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Agent-accessible filesystem read/write and copy operations can affect local workspace files.

Mitigation: Install only for workflows that need filesystem access and keep agent access limited to the intended workspace.

Risk: Overwrite-capable copy operations can replace existing files.

Mitigation: Use dry-run previews before bulk copy operations and review overwrite targets before execution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/1215656/skills/1215656-clawdbot-filesystem-1-0-2)
- [Publisher profile](https://clawhub.ai/user/1215656)
- [Node.js runtime](https://nodejs.org/)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and JSON configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May return table, tree, list, or JSON-style filesystem summaries depending on command options.]

## Skill Version(s):

1.0.2 (source: package.json, skill.json, _meta.json; ClawHub release metadata: 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
