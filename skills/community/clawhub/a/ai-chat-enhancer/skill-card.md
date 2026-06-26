## Description: <br>
Enhances LLM chat by managing conversation history, caching responses, templating prompts, counting tokens, and tracking usage for efficient interactions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[534422530](https://clawhub.ai/user/534422530) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to improve AI chat workflows with prompt templates, reusable conversation history, response caching, token counting, and usage statistics. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad trigger wording may cause the skill to be applied in conversations where chat enhancement behavior was not intended. <br>
Mitigation: Review whether the requested task actually needs chat history, prompt templating, caching, token counting, or usage tracking before applying the skill. <br>
Risk: Conversation history and cached model responses can contain sensitive data if users store real prompts or outputs. <br>
Mitigation: Avoid storing sensitive data unless the storage location, retention period, and clearing behavior are clear; clear history and cache when no longer needed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/534422530/ai-chat-enhancer) <br>
- [Artifact SKILL.md](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, guidance] <br>
**Output Format:** [Markdown with inline command and Python code examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May describe chat history, prompt templates, response cache behavior, token counts, and usage statistics.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
