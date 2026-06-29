## Description: <br>
地鼠AI剪辑专业智能剪辑 Skill / Codex 剪辑子智能体入口，用于让 Codex、QwenClaw、OpenClaw 等 AI 代理通过地鼠AI剪辑桌面端 MCP/HTTP/Bridge 完成素材分析、抖音纪实口播剪辑方案、自动排时间线、字幕、预览、校验和导出。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dspiritai](https://clawhub.ai/user/dspiritai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and AI-agent users use this skill to operate the AICut desktop bridge for documentary-style Douyin talking-head video edits, including media analysis, timeline planning, subtitles, preview, validation, and export review. The workflow is designed for AI-assisted rough cuts and structured editing with human final review before export or publication. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide an agent to control AICut through local desktop bridge, MCP, HTTP, and CLI workflows with access to local media. <br>
Mitigation: Install only when agent control of AICut is intended, use explicit file or folder picker authorization, and avoid broad Desktop or project-root access. <br>
Risk: Timeline changes, exports, and media imports may affect local projects or produce misleading output if run without review. <br>
Mitigation: Require user confirmation before timeline overwrite or export, run project validation and export validation, and keep human final review before delivery or publication. <br>
Risk: Cloud upload and public-frame settings may expose private customer, contract, backend, chat, address, phone, vehicle, or other sensitive media. <br>
Mitigation: Review cloud upload/public-frame settings, require human confirmation for sensitive footage, and blur, omit, or avoid unconfirmed private material. <br>
Risk: The artifact references API key environment variables for optional cloud and vision services. <br>
Mitigation: Keep API keys only in environment variables or server-side configuration and do not write secrets into skill files, frontend code, or public repositories. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/dspiritai/aicut-editing-assistant) <br>
- [Publisher profile](https://clawhub.ai/user/dspiritai) <br>
- [SKILL.md](artifact/SKILL.md) <br>
- [Bridge interface examples](artifact/examples.md) <br>
- [AICut editing reference](artifact/reference.md) <br>
- [Douyin documentary editing style JSON](artifact/dishu-douyin-documentary.skill.json) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline JSON, JavaScript, and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May direct agents to call AICut MCP, HTTP, Bridge, CLI, local media, cloud upload, transcription, subtitle, validation, and export workflows.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
