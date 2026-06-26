## Description: <br>
Access 50+ LLM models through a unified OpenAI-compatible API via AceDataCloud for chat completions, streaming, function calling, and vision. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Germey](https://clawhub.ai/user/Germey) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use Ai Chat to configure agents or applications to call GPT, Claude, Gemini, DeepSeek, Grok, and other models through AceDataCloud's OpenAI-compatible chat completions endpoint. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts, images or image URLs, tool definitions, and request metadata are sent to AceDataCloud and may reach downstream model providers. <br>
Mitigation: Use the skill only when that data transfer is approved, and avoid secrets or regulated data unless organizational privacy and retention requirements are satisfied. <br>
Risk: The skill requires an AceDataCloud API token and uses token-based billing. <br>
Mitigation: Use a dedicated revocable token, keep it out of code and logs, rotate it if exposed, and monitor billing for unexpected usage. <br>


## Reference(s): <br>
- [ClawHub Ai Chat release](https://clawhub.ai/Germey/acedatacloud-ai-chat) <br>
- [AceDataCloud chat completions endpoint](https://api.acedata.cloud/v1/chat/completions) <br>
- [AceDataCloud OpenAI-compatible API base](https://api.acedata.cloud/v1) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with bash, Python, JSON request examples, and OpenAI-compatible response examples.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires ACEDATACLOUD_API_TOKEN; output may include model choices, request parameters, streaming guidance, function-calling examples, and vision request examples.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata; artifact metadata reports 1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
