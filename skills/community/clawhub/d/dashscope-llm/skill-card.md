## Description: <br>
DashScope LLM sends a single-turn chat prompt to Alibaba Cloud DashScope through its OpenAI-compatible API and prints the model response. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[pengzhendong](https://clawhub.ai/user/pengzhendong) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill for quick DashScope LLM checks, prompt experiments, and simple one-shot text generation from a terminal. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompt text is sent to Alibaba Cloud DashScope. <br>
Mitigation: Use only content approved for that service and avoid passwords, API keys, personal data, or confidential business content unless sharing is authorized. <br>
Risk: The CLI reads DASHSCOPE_API_KEY from the environment. <br>
Mitigation: Keep the API key out of prompts, logs, command history, and committed files. <br>


## Reference(s): <br>
- [DashScope OpenAI-compatible API endpoint](https://dashscope.aliyuncs.com/compatible-mode/v1) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [Plain text from stdout with Markdown usage guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Single-turn requests only; no streaming, tool calling, structured output handling, or advanced retry management.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
