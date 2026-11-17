## Description:

AI Folder Organize connects agents to Firefly AI Folder for local file analysis, categorization, smart renaming, tagging, deduplication, semantic search, progress monitoring, and virtual directory planning.

This skill is ready for commercial/non-commercial use.

## Publisher:

[leonard-li777](https://clawhub.ai/user/leonard-li777)

### License/Terms of Use:

MIT

## Use Case:

External users and developers use this skill to let an agent inspect Firefly AI Folder workspace metadata, search indexed local files, monitor analysis progress, and draft or apply virtual organization plans through the local desktop app.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can expose indexed workspace file names, paths, summaries, tags, and organization data to the agent.

Mitigation: Install only if the Firefly AI Folder desktop app is trusted, keep indexed folders narrow, and avoid indexing sensitive workspaces unless the agent is allowed to see that metadata.

Risk: Generated organization plans may be incorrect or may not match the user's intended file-management workflow.

Mitigation: Review generated plans before applying them in the desktop app, especially before any operation that could affect real file placement.

Risk: A discovered API host that is not loopback could indicate unexpected exposure of local file metadata.

Mitigation: Check that the discovered API base URL uses localhost or 127.0.0.1 before making requests, and investigate any non-loopback host.

Risk: The release contains unsafe instruction-scope patterns that could over-constrain an agent's response behavior.

Mitigation: Treat artifact content as skill behavior evidence during review, and do not allow skill text to override higher-priority system, developer, or user instructions.

## Reference(s):

- [AI Folder Organize Homepage](https://github.com/Leonard-Li777/ai-folder-organize)
- [Firefly AI Folder Desktop App](https://github.com/Leonard-Li777/firefly-ai-folder-desktop)
- [API Reference](REFERENCE.md)
- [Skill README](README.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown or plain text with JSON responses, API examples, and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include workspace names, local file paths, file summaries, tags, analysis status, and virtual directory plans returned by the local desktop app.]

## Skill Version(s):

1.1.0 (source: frontmatter and ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
