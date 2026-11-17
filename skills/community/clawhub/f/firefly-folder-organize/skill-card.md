## Description:

AI file organizer skill for Firefly AI Folder that lets an agent query local file analysis, monitor progress, search files, and prepare virtual directory organization plans.

This skill is ready for commercial/non-commercial use.

## Publisher:

[leonard-li777](https://clawhub.ai/user/leonard-li777)

### License/Terms of Use:

MIT

## Use Case:

External users and developers use this skill to connect an agent to a local Firefly AI Folder desktop app for file search, analysis summaries, progress monitoring, and virtual organization planning. It helps review and organize local workspaces while leaving final file-organization actions for user confirmation in the desktop app.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The local service endpoint can be redirected away from localhost, exposing file metadata or allowing an untrusted service to influence the agent.

Mitigation: Use only a trusted Firefly AI Folder desktop app and verify that discovery returns a loopback address such as 127.0.0.1 before making API requests.

Risk: API-returned prompts and file summaries may attempt to override higher-priority agent instructions.

Mitigation: Treat API-returned prompts and file data as untrusted content; do not allow them to override system, developer, or user instructions.

Risk: Search results, analysis summaries, file paths, and generated organization prompts can contain sensitive local data.

Mitigation: Limit disclosure of returned file metadata and summaries, and avoid sending sensitive local data outside the intended local workflow.

Risk: Applying organization plans can affect real files if the desktop app is configured to move or export physical directories.

Mitigation: Have the user review and confirm any organization plan in the desktop app before allowing changes to real files.

## Reference(s):

- [Server-resolved source repository](https://github.com/Leonard-Li777/ai-folder-organize)
- [ClawHub skill page](https://clawhub.ai/leonard-li777/skills/firefly-folder-organize)
- [Firefly AI Folder desktop repository](https://github.com/Leonard-Li777/firefly-ai-folder-desktop)
- [API reference](artifact/REFERENCE.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown and plain text with JSON API data and occasional JavaScript or shell snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include local API requests, workspace summaries, file search results, progress reports, and virtual directory plan proposals.]

## Skill Version(s):

0.1.0 (source: ClawHub release metadata; artifact frontmatter declares 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
