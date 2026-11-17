## Description:

Provides agent-facing filesystem operations for listing, searching, batch copying, tree display, and directory analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gtrusler](https://clawhub.ai/user/gtrusler)

### License/Terms of Use:

MIT

## Use Case:

Developers and agents use this skill to inspect directories, search filenames or file contents, copy matched files with dry-run safeguards, and summarize filesystem structure.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requests broad read-write local filesystem access, including search and copy behavior that can touch private or unintended directories.

Mitigation: Use dry runs before copy operations, verify destination paths carefully, avoid broad recursive searches over sensitive directories, and treat overwrite operations as requiring explicit review.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/gtrusler/skills/clawdbot-filesystem)
- [Node.js](https://nodejs.org/)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown or terminal text with command examples and optional table, list, tree, or JSON outputs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include file lists, search matches with context, copy previews, tree output, and directory statistics.]

## Skill Version(s):

1.0.2 (source: package.json and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
