## Description: <br>
Exports Feishu or Lark cloud documents and wiki pages to Markdown, PDF, or Word through feishu-cli. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[GISwilson](https://clawhub.ai/user/GISwilson) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to export Feishu or Lark documents and wiki pages into local Markdown for review, editing, or version control, and to trigger PDF or Word exports when needed. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security scan flagged the release as suspicious because it includes an under-disclosed workflow that can upload local files into Feishu. <br>
Mitigation: Use only a trusted feishu-cli, grant least-privilege Feishu credentials, and do not run import-file behavior unless you intentionally want to upload a local file. <br>
Risk: The skill can export documents and download assets from Feishu or Lark workspaces, which may include sensitive content. <br>
Mitigation: Use it only with documents you are authorized to export and store generated files in an appropriate local path. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/GISwilson/feishu-cli-export) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Markdown, Files, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and exported Markdown, PDF, or Word files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May read exported files and show file size and content previews; optional image downloads can write local asset files.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
