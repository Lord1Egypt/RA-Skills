## Description: <br>
Provides a command-line wrapper for sending prompts to the DeepSeek chat API using selected DeepSeek models. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bseye520](https://clawhub.ai/user/bseye520) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agents can use this skill to send a prompt to DeepSeek's chat API from a Node.js command and receive the model response and token usage. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The release includes an apparent DeepSeek API key in config.env. <br>
Mitigation: Remove or ignore the bundled value, provide your own key through a secret mechanism, and rotate any exposed credential before use. <br>
Risk: User prompts are sent to the DeepSeek third-party API. <br>
Mitigation: Avoid sending secrets, regulated data, or confidential content unless that provider use is approved for the deployment. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/bseye520/deepseek-chat) <br>
- [DeepSeek platform](https://platform.deepseek.com) <br>
- [DeepSeek API endpoint](https://api.deepseek.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration] <br>
**Output Format:** [Plain text terminal output with token usage details when returned by the API.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a DEEPSEEK_API_KEY environment variable and network access to api.deepseek.com.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
