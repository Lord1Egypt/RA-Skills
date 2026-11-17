## Description:

Docx Editing helps agents surgically edit existing .docx files with formatting preservation and tracked changes through the local Safe-DOCX MCP server.

This skill is ready for commercial/non-commercial use.

## Publisher:

[stevenobiajulu](https://clawhub.ai/user/stevenobiajulu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, editors, legal reviewers, and other document-focused users use this skill to read, revise, comment on, compare, and save existing Word documents while preserving formatting and producing tracked-change redlines.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The MCP server can access DOCX files under the user's home directory and system temp folders.

Mitigation: Use the skill only with explicit document paths, keep edits directed at intended input files, and avoid running it in workspaces containing unrelated sensitive documents.

Risk: The default npx connector performs a one-time npm registry fetch during setup, which may be unsuitable for restricted environments.

Mitigation: Use the pinned or vendored installation path, review the package or source before use, and invoke the installed safe-docx binary directly where registry access is not allowed.

Risk: Automated document edits or redlines can introduce incorrect language into contracts, agreements, or other high-impact documents.

Mitigation: Review clean and tracked-change outputs before relying on them, especially for legal, financial, or customer-facing documents.

## Reference(s):

- [Safe-DOCX GitHub repository](https://github.com/UseJunior/safe-docx)
- [Safe-DOCX npm package](https://www.npmjs.com/package/@usejunior/safe-docx)
- [Safe-DOCX stdio server source](https://github.com/UseJunior/safe-docx/blob/main/packages/safe-docx/src/server.ts)
- [Safe-DOCX changelog](https://github.com/UseJunior/safe-docx/blob/main/CHANGELOG.md)
- [Connector setup guide](CONNECTORS.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline commands, JSON connector snippets, and agent tool-use instructions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May direct the agent to save clean and tracked-change DOCX files, produce structured revision JSON, or provide setup commands for MCP connectors.]

## Skill Version(s):

0.3.0 (source: server evidence and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
