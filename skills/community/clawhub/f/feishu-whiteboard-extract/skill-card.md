## Description: <br>
Extracts Feishu Whiteboard image-node file tokens and exports board images so agents can support download, OCR, and archive workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[forevershu](https://clawhub.ai/user/forevershu) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill to extract image tokens from Feishu Whiteboards, download media for OCR, and export full-board images for review or archival handoff. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses Feishu app credentials to access whiteboards and media. <br>
Mitigation: Use a dedicated least-privilege Feishu app and share only the specific whiteboards needed with that app. <br>
Risk: The raw node export can print full board node data to stdout or logs. <br>
Mitigation: Run export_nodes_raw.js only when full node data is intentionally needed, and keep logs out of shared or long-retention locations. <br>
Risk: The release includes dependency lock entries resolved from a non-HTTPS registry mirror. <br>
Mitigation: Regenerate dependencies from an HTTPS registry before deploying in a sensitive environment. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance, files] <br>
**Output Format:** [Markdown guidance with bash commands and JSON outputs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Scripts can output image-token JSON, downloaded media paths, raw node JSON, or exported board image files.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
