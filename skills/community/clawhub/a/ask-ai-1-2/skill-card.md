## Description: <br>
When an agent is stuck, this skill automatically asks Doubao, Qianwen, Kimi, or DeepSeek for a concrete solution and then applies the response. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[danielwang20150225-source](https://clawhub.ai/user/danielwang20150225-source) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill when an OpenClaw agent cannot confidently solve a task and needs structured help from external AI chat services. It organizes the question, submits it through a persisted browser profile, polls for an answer, and decides whether to execute, follow up, or switch providers. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Task details may be sent to third-party AI chat services through persisted logged-in browser sessions. <br>
Mitigation: Use the skill only for information that is approved for those services, and add confirmation or redaction before sending private code, credentials, personal data, business-sensitive material, or regulated information. <br>
Risk: Responses from external models may be incomplete, misleading, or unsuitable for direct execution. <br>
Mitigation: Review model output before applying changes, especially commands, code edits, and recommendations that affect security, data, or production systems. <br>
Risk: The skill can keep records of model replies and execution state. <br>
Mitigation: Define a memory-retention policy and avoid storing sensitive prompts or responses unless retention is explicitly approved. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/danielwang20150225-source/ask-ai-1-2) <br>
- [Doubao Chat](https://www.doubao.com/chat/) <br>
- [Qianwen](https://qianwen.aliyun.com) <br>
- [Kimi](https://kimi.moonshot.cn) <br>
- [DeepSeek](https://www.deepseek.com) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Markdown, Code] <br>
**Output Format:** [Markdown with command snippets, status markers, and summarized external model responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include follow-up questions, execution decisions, and memory notes about provider failures.] <br>

## Skill Version(s): <br>
1.2.4 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
