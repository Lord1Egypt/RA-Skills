## Description: <br>
Configure Claude Code to use custom models such as DeepSeek, GLM, Qwen, or other OpenAI-compatible endpoints when users need to switch API provider, model, or endpoint settings. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[moonbird0423](https://clawhub.ai/user/moonbird0423) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to configure Claude Code for a chosen third-party model provider by setting endpoint, model, and API key values in Claude Code environment and configuration locations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill persistently changes Claude Code provider settings and may leave stale provider configuration in user-level environment or config files. <br>
Mitigation: Review the target files before and after changes, keep a backup of existing Claude Code configuration, and document how to restore the previous provider settings. <br>
Risk: The workflow handles API keys and stores them in Claude Code configuration with weak safety controls. <br>
Mitigation: Treat the API key as a secret, avoid copied or untrusted values, prefer restrictive file permissions, and rotate the key if it may have been exposed. <br>
Risk: On Windows, copied or untrusted values are passed into persistent user environment variable commands. <br>
Mitigation: Use only trusted endpoint, model, and key values, and manually inspect commands before running them. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/moonbird0423/claude-code-model) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration guidance] <br>
**Output Format:** [Markdown with inline shell commands, JSON snippets, and Python script usage] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include commands or configuration values that contain sensitive API keys.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
