## Description: <br>
Gradio-based chat interface for Ollama that creates a web chat UI with model selection, streaming responses, and multi-session management through ChatManager. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wangyendt](https://clawhub.ai/user/wangyendt) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill to work with pywayne.llm.chat_ollama_gradio when launching a local Gradio chat UI for Ollama models with session switching, model discovery, and streaming conversation history. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The Gradio server may be network-accessible if launched with a broad host binding. <br>
Mitigation: Bind the server to localhost, such as 127.0.0.1, unless LAN access is intentional. <br>
Risk: The workflow depends on local pywayne, gradio, and Ollama components. <br>
Mitigation: Install and run the required components only from sources you trust. <br>
Risk: Chat content and session history may remain in memory while the app is running. <br>
Mitigation: Avoid entering sensitive content unless temporary in-memory retention is acceptable. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wangyendt/chat-ollama-gradio) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with Python code blocks and configuration tables] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes local Ollama endpoint, Gradio launch settings, model selection, and in-memory session history guidance.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
