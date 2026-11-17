## Description:

Installs GitNexus, configures its MCP service, and builds a code knowledge graph for the current project.

This skill is ready for commercial/non-commercial use.

## Publisher:

[babywhale](https://clawhub.ai/user/babywhale)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to set up GitNexus for an existing project, configure MCP integration, index the repository, and verify the resulting code knowledge graph.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Fallback and troubleshooting commands may execute unpinned GitNexus packages through npx.

Mitigation: Use the pinned global install command or an explicitly pinned `npx gitnexus@1.6.5` command before running setup, status, or analyze.

Risk: The troubleshooting flow can commit all local files with `git add . && git commit`, which may include secrets or private files.

Mitigation: Review `.gitignore`, inspect `git status`, and confirm no sensitive files are staged before committing.

## Reference(s):

- [Node.js](https://nodejs.org/)
- [nvm](https://github.com/nvm-sh/nvm)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guides project-root detection, Node.js version checks, GitNexus installation, MCP setup, repository indexing, and verification steps.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
