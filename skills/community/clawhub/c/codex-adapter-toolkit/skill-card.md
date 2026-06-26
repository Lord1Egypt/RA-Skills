## Description: <br>
Codex Adapter Toolkit helps agents configure and operate local API adapters for switching Codex among providers such as DeepSeek, MiniMax, OpenAI, Gemini, Grok, Ollama, Claude Direct, and OpenRouter. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[luis1213899](https://clawhub.ai/user/luis1213899) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to configure local Codex API adapters, switch model providers, manage failover, and handle provider credentials for AI coding workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles API keys and provider configuration for local adapters, so secrets could be exposed if written to source control, logs, or permissive settings files. <br>
Mitigation: Keep API keys out of source control and logs, restrict settings file permissions, and review generated commands before use. <br>
Risk: Backup and restore operations can overwrite local adapter settings. <br>
Mitigation: Create a fresh backup before restore operations and verify the target configuration before applying changes. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/luis1213899/codex-adapter-toolkit) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration] <br>
**Output Format:** [Markdown with inline shell commands and configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include local adapter commands, provider choices, health checks, backup and restore steps, and secret-handling guidance.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
