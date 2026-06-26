## Description: <br>
AI-powered content summarization and project retrospective tool with support for multiple large-model APIs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nidhov01](https://clawhub.ai/user/nidhov01) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and knowledge workers use this skill to summarize daily work, meetings, articles, and project material, with optional LLM-backed summaries and project retrospectives. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: User text can be sent to external AI providers. <br>
Mitigation: Avoid confidential content unless the selected provider and its data policy are trusted; use limited-scope API keys. <br>
Risk: Summaries and source content may be stored on disk. <br>
Mitigation: Inspect or delete ~/.ai_summary.db when it may contain sensitive material. <br>
Risk: The artifact references llm_client.py and llm_config.py, which were not included in the submitted files. <br>
Mitigation: Review the missing support files before installing or using the skill. <br>
Risk: Dependency installation can change the local Python environment. <br>
Mitigation: Install dependencies in a virtual environment with pinned versions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/nidhov01/06-ai) <br>
- [Zhipu AI API keys](https://open.bigmodel.cn/usercenter/apikeys) <br>
- [OpenAI API keys](https://platform.openai.com/api-keys) <br>
- [Anthropic Console](https://console.anthropic.com/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Text and Markdown summaries, Python dictionary results, shell commands, and configuration snippets.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can use external LLM providers when API keys are configured; falls back to basic local summarization when keys are unavailable.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata; artifact frontmatter reports 2.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
