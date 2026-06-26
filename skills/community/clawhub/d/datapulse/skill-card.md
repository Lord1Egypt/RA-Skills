## Description: <br>
Cross-platform content collection, web search, trending topics, confidence scoring, and watch/triage workflows for assistant and agent usage. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sunyifei83](https://clawhub.ai/user/sunyifei83) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, analysts, and agent builders use DataPulse to read and batch-read URLs, search web and trend sources, collect cross-platform signals, and maintain watch, alert, triage, and story-evidence workflows for assistant use. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad network access can send requests to target URLs and optional external APIs. <br>
Mitigation: Use only trusted URLs and configure API keys such as JINA_API_KEY, TAVILY_API_KEY, and GROQ_API_KEY only for environments where outbound access is acceptable. <br>
Risk: Optional browser automation can reuse authenticated WeChat or Xiaohongshu sessions stored locally. <br>
Mitigation: Enable Playwright login sessions only when needed, protect ~/.datapulse/sessions/, and clear session files after use on shared machines. <br>
Risk: Subprocess-backed workflows and the manual upgrade command can execute local tools or package updates. <br>
Mitigation: Review requested backend commands and run upgrade actions only from a trusted shell and package source. <br>
Risk: Alert routes can POST to user-configured webhook, Feishu, or Telegram destinations. <br>
Mitigation: Configure alert destinations deliberately and avoid routing sensitive collected content to untrusted endpoints. <br>


## Reference(s): <br>
- [DataPulse on ClawHub](https://clawhub.ai/sunyifei83/datapulse) <br>
- [Publisher profile](https://clawhub.ai/user/sunyifei83) <br>
- [DataPulse repository](https://github.com/sunyifei83/DataPulse) <br>
- [OpenClaw metadata requirements](artifact/SKILL.md) <br>
- [Skill manifest](artifact/datapulse_skill/manifest.json) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, configuration, guidance] <br>
**Output Format:** [Structured text, JSON-compatible dictionaries, Markdown memory artifacts, and CLI output.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May persist session files under ~/.datapulse/sessions/ and workflow data under a local data/ folder when users enable those workflows.] <br>

## Skill Version(s): <br>
0.8.1 (source: server release evidence and SKILL.md heading; pyproject.toml reports 0.8.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
