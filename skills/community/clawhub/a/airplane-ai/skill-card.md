## Description: <br>
Give LM Studio or Ollama users a browser-based AI chat interface that works completely offline. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[robinflw](https://clawhub.ai/user/robinflw) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and local LLM users use AirplaneAI to launch an offline browser chat interface for LM Studio, Ollama, llama.cpp, or vLLM while keeping chat traffic on the local machine. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Model output can trigger unrestricted local file reads in the chat session. <br>
Mitigation: Use only trusted local LLM endpoints, avoid chats involving secrets, and disable or restrict the READ feature until explicit approval and path limits are added. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/robinflw/airplane-ai) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a trusted local OpenAI-compatible LLM endpoint and may include optional persona-file setup.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
