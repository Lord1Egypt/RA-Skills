## Description: <br>
Ask LLM Council a question directly from Telegram or chat and return the chairman's synthesized answer without opening the web UI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jeadland](https://clawhub.ai/user/jeadland) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Employees, external users, and developers use this skill to send a quick question to a trusted local LLM Council setup and receive the synthesized final answer in chat. It is suited for fast decision support when the full web discussion is not needed. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts may be processed by connected models and may appear in the local backend web UI or logs. <br>
Mitigation: Avoid sending secrets, credentials, or sensitive personal data through /council. <br>
Risk: The skill depends on a local LLM Council backend that receives the user's question. <br>
Mitigation: Install and run it only when you trust the local backend and its connected model configuration. <br>


## Reference(s): <br>
- [Ask Council ClawHub page](https://clawhub.ai/jeadland/ask-council) <br>
- [LLM Council repository](https://github.com/jeadland/llm-council) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Guidance] <br>
**Output Format:** [Terminal text response with a synthesized answer and discussion link] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates a new conversation for each question and times out after 120 seconds.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
