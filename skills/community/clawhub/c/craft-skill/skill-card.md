## Description:

Create and format Craft documents reliably via the Craft MCP v2 unified API (craft_write / craft_read), including document creation, editing, formatting, and structured content workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mabaty](https://clawhub.ai/user/mabaty)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and productivity-focused users use this skill to have an agent create, edit, format, and verify Craft documents, notes, tasks, collections, whiteboards, comments, and page styling through Craft MCP v2.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide an agent to modify real Craft production data, including broad write and delete operations.

Mitigation: Use it only when production Craft changes are acceptable, require explicit confirmation for destructive or high-impact writes, and keep recoverable copies of important content.

Risk: The documented delete-and-recreate rewrite path can remove existing documents or content if used without a reliable rollback plan.

Mitigation: Prefer reversible edits where possible, verify rollback before considering work complete, and avoid full rewrites unless the user has approved the recovery plan.

Risk: Batched commands may partially apply before a failure, leaving Craft content in an intermediate state.

Mitigation: Read back affected documents after writes, verify expected ordering and content, and repair or revert partial changes before finishing.

## Reference(s):

- [Source repository](https://github.com/mabaty/craft-skill)
- [ClawHub skill page](https://clawhub.ai/mabaty/skills/craft-skill)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with Craft MCP command strings and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce Craft MCP read/write commands that create, update, move, delete, or verify production Craft content.]

## Skill Version(s):

0.1.0 (source: server release metadata); artifact frontmatter reports 2.0.2

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
