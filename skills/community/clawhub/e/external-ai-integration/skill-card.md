## Description: <br>
Leverage external AI models such as ChatGPT, Claude, Gemini, and Hugging Face as on-demand tools through browser automation and optional API calls. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[konscious0beast](https://clawhub.ai/user/konscious0beast) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent operators use this skill to route selected prompts to external AI services for second opinions, summarization, translation, code review, brainstorming, and specialized model outputs while keeping the main assistant in control of the workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Selected prompts may be sent to external AI providers through logged-in accounts or a Hugging Face token. <br>
Mitigation: Use only with content approved for those providers, and avoid secrets, private customer data, regulated data, or proprietary code unless the provider is approved for that content. <br>
Risk: Manual tests can expose Hugging Face token prefixes in logs. <br>
Mitigation: Avoid running the manual test script in shared logs, and keep tokens in approved secret storage or environment variables. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/konscious0beast/external-ai-integration) <br>
- [ChatGPT web interface](https://chatgpt.com) <br>
- [Hugging Face Inference API model endpoint](https://api-inference.huggingface.co/models/{model}) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with code and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May require logged-in external AI accounts or an HF_TOKEN for Hugging Face API calls.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
