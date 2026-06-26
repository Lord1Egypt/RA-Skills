## Description: <br>
Surgically edit existing .docx files with formatting preservation and tracked changes through the local Safe-DOCX MCP server. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[stevenobiajulu](https://clawhub.ai/user/stevenobiajulu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, legal operations teams, and document-review agents use this skill to read, locate, edit, comment on, compare, and save existing Word documents while preserving formatting and producing clean or tracked-change outputs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Accidental edits can change important Word documents or target the wrong file. <br>
Mitigation: Work on copies or save to a new output path, verify the exact file before editing, and review the clean and redline outputs before sharing. <br>
Risk: The default connector uses a local npm package, so install-time package trust and unexpected upgrades matter. <br>
Mitigation: Keep the Safe-DOCX package version pinned, review the changelog before upgrades, and use the documented offline or vendored install path for high-security environments. <br>
Risk: Accepting tracked changes removes revision markup and can obscure what changed. <br>
Mitigation: Accept tracked changes only when intentionally finalizing a document, and retain a redline copy when review history is needed. <br>


## Reference(s): <br>
- [ClawHub Docx Editing release](https://clawhub.ai/stevenobiajulu/docx-editing) <br>
- [Safe-DOCX GitHub repository](https://github.com/UseJunior/safe-docx) <br>
- [Safe-DOCX npm package](https://www.npmjs.com/package/@usejunior/safe-docx) <br>
- [Safe-DOCX changelog](https://github.com/UseJunior/safe-docx/blob/main/CHANGELOG.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline JSON and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces document-editing plans, MCP tool call guidance, connector configuration, and saved .docx outputs through the configured local MCP server.] <br>

## Skill Version(s): <br>
0.3.0 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
