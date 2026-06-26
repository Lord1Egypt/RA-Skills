## Description: <br>
Feishu Docs helps an agent read, create, update, delete, import, and list Feishu cloud documents from Claude Code. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[upupc](https://clawhub.ai/user/upupc) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and operators use this skill to manage Feishu cloud documents from an agent-assisted command line workflow, including reading document content, creating or importing documents, listing folders, updating content, and deleting documents. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can read, write, import, update, and delete Feishu documents using tenant app credentials. <br>
Mitigation: Use a least-privilege Feishu self-built app, keep FEISHU_APP_SECRET out of version control, and verify document and folder tokens before running commands. <br>
Risk: The default update mode can overwrite existing document content. <br>
Mitigation: Prefer --append when possible and export or back up important documents before using overwrite update operations. <br>
Risk: Delete operations can remove Feishu documents. <br>
Mitigation: Confirm the target document token and keep the command's force confirmation requirement in place for destructive deletes. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/upupc/feishu-docs-v2) <br>
- [Project homepage](https://github.com/upupc/feishu-docs) <br>
- [Feishu Open Platform](https://open.feishu.cn) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, files, shell commands, configuration] <br>
**Output Format:** [Command-line output with optional JSON, Markdown, text, and local file artifacts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Node.js and Feishu app credentials in FEISHU_APP_ID and FEISHU_APP_SECRET.] <br>

## Skill Version(s): <br>
0.1.3 (source: server release metadata; artifact frontmatter and package.json report 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
