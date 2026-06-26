## Description: <br>
Checks and reports a DeepSeek API account's balance and availability using a configured API key. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[liflife](https://clawhub.ai/user/liflife) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and API users use this skill to query DeepSeek account balance, granted balance, topped-up balance, and account availability from a terminal. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: If DEEPSEEK_API_KEY is unset, the skill can send ANTHROPIC_AUTH_TOKEN to DeepSeek as a fallback credential. <br>
Mitigation: Set DEEPSEEK_API_KEY explicitly before use, unset ANTHROPIC_AUTH_TOKEN in the execution environment, or remove the fallback from the command. <br>
Risk: The skill requires a sensitive API credential to query account balance. <br>
Mitigation: Run it only in a trusted shell session and avoid pasting or logging the API key. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/liflife/deepseek-balance) <br>
- [DeepSeek balance API endpoint](https://api.deepseek.com/user/balance) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with Bash commands, embedded Python JSON parsing, and sample terminal output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a DeepSeek API key in the environment before use.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
