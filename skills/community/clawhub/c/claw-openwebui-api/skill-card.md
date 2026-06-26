## Description: <br>
整合 Open WebUI RAG 知識庫 API，讓 OpenClaw 能自動上傳文件和查詢知識庫。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dolphins1123](https://clawhub.ai/user/dolphins1123) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to connect an agent to a trusted Open WebUI instance so it can list models and knowledge bases, upload files, search RAG content, and send chat requests. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: API tokens, prompts, and selected files can be sent to a hardcoded Open WebUI server if OPENWEBUI_URL is not explicitly set. <br>
Mitigation: Set OPENWEBUI_URL to a trusted Open WebUI instance before running commands and verify it is not falling back to 192.168.0.176. <br>
Risk: Uploaded files and chat prompts are sent to the configured Open WebUI service for storage and processing. <br>
Mitigation: Use a trusted server, prefer a scoped API token when available, and upload only files that are appropriate for that Open WebUI instance. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/dolphins1123/claw-openwebui-api) <br>
- [Open WebUI documentation](https://docs.openwebui.com/) <br>
- [Open WebUI API endpoint reference](https://docs.openwebui.com/reference/api-endpoints/) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell command examples and JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires OPENWEBUI_URL and OPENWEBUI_API_KEY for Python scripts; shell usage falls back to a default Open WebUI URL if OPENWEBUI_URL is unset.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata and artifact frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
