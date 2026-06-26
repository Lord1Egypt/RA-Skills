## Description: <br>
Use DeepSeek V4 Flash and Pro from the command line for one-shot Q&A, thinking mode, and multi-turn chat through an OpenAI-compatible API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jiajiaoy](https://clawhub.ai/user/jiajiaoy) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to call DeepSeek V4 Flash or Pro from a terminal for Q&A, writing, coding, summaries, reasoning tasks, and multi-turn chat. It is useful when an agent needs practical shell commands and guidance for using DeepSeek's OpenAI-compatible API. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts, system prompts, and chat history are sent to DeepSeek's external API. <br>
Mitigation: Use the skill only for data approved for DeepSeek API processing, and avoid confidential or regulated data unless that use is explicitly approved. <br>
Risk: The skill requires the sensitive DEEPSEEK_API_KEY credential. <br>
Mitigation: Keep the key private, store it in an appropriate local secret or environment mechanism, and avoid exposing it in shared shell history, logs, or support transcripts. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jiajiaoy/deepseek-v4) <br>
- [DeepSeek API documentation](https://api-docs.deepseek.com) <br>
- [DeepSeek API keys](https://platform.deepseek.com/api_keys) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Plain text and streamed terminal output with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses DEEPSEEK_API_KEY and may stream model output from DeepSeek's external API.] <br>

## Skill Version(s): <br>
1.0.1 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
