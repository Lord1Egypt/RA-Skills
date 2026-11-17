## Description: <br>
Helps agents append and structure content in Feishu documents, including heading-based block writing, batch block operations, and format conversion. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thcjp](https://clawhub.ai/user/thcjp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to guide an agent through Feishu document writing tasks such as appending Markdown content, splitting long documents by heading, and managing document blocks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can require Feishu document credentials and may authorize an agent to create, update, export, or delete document blocks. <br>
Mitigation: Use least-privilege Feishu app permissions and require explicit confirmation before destructive, bulk, or export operations. <br>
Risk: The release is described as append-focused, while the security summary says the behavior expands into broader document management without clear safeguards. <br>
Mitigation: Review the skill as a broad Feishu document management guide and constrain agent use to approved document actions before installation. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JSON, YAML, Python, and shell examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May require Feishu application credentials and agent permission to execute document-management commands.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata; artifact frontmatter lists 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
