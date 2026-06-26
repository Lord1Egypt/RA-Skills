## Description: <br>
Exports Feishu docx documents to local Markdown with document formatting, links, and images saved for local use. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[technologyliu](https://clawhub.ai/user/technologyliu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, operators, and Feishu workspace users can use this skill to configure a Feishu app and export accessible docx documents into local Markdown files for archival, migration, or downstream editing. The included script currently supports single docx links; folder batch export is advertised but not implemented in the script evidence. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill overstates batch and folder export behavior compared with the included script. <br>
Mitigation: Treat the release as a single-document exporter unless folder export support is verified in updated code. <br>
Risk: The skill requires Feishu app credentials and read permissions that can expose document contents. <br>
Mitigation: Use a dedicated low-privilege Feishu app, grant only needed read permissions, and keep credentials out of shared logs or exported files. <br>
Risk: Exported Markdown and images are written to a local directory and may contain sensitive document content. <br>
Mitigation: Choose a deliberate output directory, apply normal data handling controls, and review exported files before sharing. <br>


## Reference(s): <br>
- [Feishu app configuration guide](references/config.md) <br>
- [Feishu Open Platform](https://open.feishu.cn/) <br>
- [ClawHub skill page](https://clawhub.ai/technologyliu/feishu-doc-batch-export) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Files, Shell commands, Configuration] <br>
**Output Format:** [Markdown files with downloaded image assets and optional HTML files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires FEISHU_APP_ID and FEISHU_APP_SECRET environment variables and a Feishu app with appropriate document read permissions.] <br>

## Skill Version(s): <br>
1.0.0 (source: release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
