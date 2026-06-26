## Description: <br>
Implements exact filename search, fuzzy filename search, semantic file search, and image-based image search for Alibaba Cloud PDS. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sdk-team](https://clawhub.ai/user/sdk-team) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and enterprise users use this skill to search Alibaba Cloud PDS drives by filename, metadata, semantic content, and image similarity. The skill also guides related PDS file operations, including upload, download, and document or media analysis workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Credential-backed PDS access can authorize more than search, including file upload, download, analysis, and cloud writes. <br>
Mitigation: Use a least-privilege or short-lived Alibaba Cloud account and confirm the configured PDS domain, user, and target space before running workflows. <br>
Risk: Upload, download, and analysis workflows can move sensitive files between local storage and PDS or write result files locally. <br>
Mitigation: Review every source path, destination path, drive, file ID, and output location before execution, and avoid sensitive files unless the user explicitly selects them. <br>
Risk: Analysis and download flows may create signed-URL result files that can expose access to PDS content. <br>
Mitigation: Protect raw JSON outputs and signed URLs, delete them when no longer needed, and avoid sharing them in conversation or logs. <br>
Risk: The skill changes Aliyun CLI execution mode and relies on plugin updates. <br>
Mitigation: Review CLI and plugin updates before running them, ensure AI-mode is disabled at every exit point, and keep CLI configuration files protected. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/sdk-team/alibabacloud-pds-multimodal-search) <br>
- [PDS Multimodal Search Skill](SKILL.md) <br>
- [Aliyun CLI Installation & Configuration Guide](references/cli-installation-guide.md) <br>
- [PDS Aliyun CLI Configuration Guide](references/config.md) <br>
- [PDS Drive Concepts and API Reference](references/drive.md) <br>
- [PDS File Search](references/search-file.md) <br>
- [Alibaba Cloud PDS Visual Similar Search Guide](references/visual-similar-search.md) <br>
- [PDS Document and Audio/Video Analysis](references/multianalysis-file.md) <br>
- [PDS File Upload Guide](references/upload-file.md) <br>
- [PDS File Download Guide](references/download-file.md) <br>
- [RAM Permission Requirements](references/ram-policies.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, shell commands, configuration, JSON, files] <br>
**Output Format:** [Markdown guidance with inline shell commands, JSON query payloads, and helper-script outputs.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce local downloaded files, formatted analysis text, raw JSON analysis results, or PPTX files when requested by the workflow.] <br>

## Skill Version(s): <br>
0.0.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
