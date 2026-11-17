## Description:

Connects agents to Meego, the Feishu Project Bytedance internal version, through an MCP service with OAuth authentication for querying and managing tasks, views, and work items.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wadxm](https://clawhub.ai/user/wadxm)

### License/Terms of Use:

MIT-0

## Use Case:

Employees and developers working in the Feishu Project or Meego environment use this skill to authenticate through OAuth and query, create, update, or transition Meego work items and views.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: OAuth credential files may be exposed if copied into chat, logs, temporary files, or locations outside the mcporter credential store.

Mitigation: Prefer the browser OAuth flow, require explicit user confirmation for credential operations, keep credentials out of chat and logs, store them only in ~/.mcporter/credentials.json, and immediately remove temporary files.

Risk: Authentication and Meego operations run an unpinned npm package through npm or npx.

Mitigation: Pin and review the @lark-project/meego-mcporter package version before running npm or npx commands.

Risk: OAuth access could grant broader Meego permissions than the task requires.

Mitigation: Use an OAuth account with the minimum Meego permissions needed for the intended workflow.

## Reference(s):

- [@lark-project/meego-mcporter npm package](https://www.npmjs.com/package/@lark-project/meego-mcporter)
- [Remote OAuth authorization guide](https://bytedance.larkoffice.com/wiki/UspfwpHaFi6LxQkt9xBcIS54nNg)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command snippets and JSON configuration references]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guidance can include OAuth setup steps, MCP call commands, and credential handling precautions; raw OAuth credentials should not be emitted.]

## Skill Version(s):

1.0.10 (source: SKILL.md frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
