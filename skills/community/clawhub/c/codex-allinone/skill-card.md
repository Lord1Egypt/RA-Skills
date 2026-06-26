## Description: <br>
Configures and runs Codex CLI inside ArkClaw or OpenClaw with Ark AgentPlan, Coding Plan, Kimi, DeepSeek, Ark v3, or a custom OpenAI-compatible endpoint. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bao2200220](https://clawhub.ai/user/bao2200220) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and ArkClaw or OpenClaw users use this skill to install, configure, switch, health-check, and invoke Codex CLI against supported model providers or a custom OpenAI-compatible endpoint. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can make lasting shell and Codex configuration changes, including writing entries under ~/.bashrc and ~/.codex. <br>
Mitigation: Review the setup scripts before installation, run them in a controlled environment, and confirm rollback steps for removing shell entries, profile files, and backups. <br>
Risk: The skill handles and stores sensitive provider API keys. <br>
Mitigation: Use least-privilege keys where possible, avoid shared machines, rotate keys after testing, and remove stored keys when the skill is no longer needed. <br>
Risk: The skill can start local background relay processes and route Codex traffic to the configured provider or custom endpoint. <br>
Mitigation: Confirm the selected provider and endpoint before use, monitor or stop relay processes when finished, and avoid untrusted custom endpoints. <br>
Risk: The skill may install or upgrade local packages needed for Codex CLI or relay behavior. <br>
Mitigation: Review package installation commands before running the skill and use an isolated sandbox or disposable environment when evaluating it. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/bao2200220/codex-allinone) <br>
- [Routing Flow](artifact/references/routing-flow.md) <br>
- [Third-Party Providers](artifact/references/thirdparty-providers.md) <br>
- [Troubleshooting](artifact/references/troubleshooting.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown and terminal-oriented guidance with shell commands and configuration changes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May trigger local setup scripts, provider profile changes, background relay processes, and Codex CLI execution.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
