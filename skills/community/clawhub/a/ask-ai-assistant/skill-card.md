## Description: <br>
Helps an agent escalate difficult or low-confidence tasks to named third-party AI services, then validates and summarizes candidate solutions before acting. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[danielwang20150225-source](https://clawhub.ai/user/danielwang20150225-source) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agents and developers use this skill when the primary assistant is blocked, low-confidence, or has offered an incomplete path and needs to ask external AI services for a more executable solution. It is intended to produce a checked plan, follow-up questions, and a final decision on whether to proceed. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can send user task details to third-party AI providers. <br>
Mitigation: Confirm the exact prompt before sending, remove secrets and private personal or business data, and use the named providers only with user approval. <br>
Risk: The skill may use existing browser sessions or logged-in accounts for external AI services. <br>
Mitigation: Avoid automatic cookie or session use unless intentionally approved, and stop for user action when login or captcha prompts appear. <br>
Risk: External AI responses can be incorrect, incomplete, or unsuitable for direct execution. <br>
Mitigation: Review any returned plan before acting, validate concrete steps, and preserve the skill's final self-check before closure. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/danielwang20150225-source/ask-ai-assistant) <br>
- [Doubao](https://www.doubao.com) <br>
- [Qianwen](https://qianwen.aliyun.com) <br>
- [Kimi](https://kimi.moonshot.cn) <br>
- [DeepSeek](https://www.deepseek.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, guidance] <br>
**Output Format:** [Markdown with status markers, follow-up prompts, AI response summaries, and executable guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include saved external AI responses, polling status, validation results, and final execution notes.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
