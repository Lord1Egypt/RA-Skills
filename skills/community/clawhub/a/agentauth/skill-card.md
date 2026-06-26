## Description: <br>
agentauth requires user-initiated biometric passkey approval before OpenClaw agents perform sensitive actions such as deleting files, sending emails, making purchases, or modifying system configuration. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[braga-agentauth](https://clawhub.ai/user/braga-agentauth) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to add passkey-backed human approval before an agent executes sensitive or irreversible local actions. It is intended for workflows where agent actions may affect files, credentials, external systems, purchases, or system configuration. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can mediate and execute dangerous local commands after passkey approval. <br>
Mitigation: Install only when this command-execution authority is intended, and require approvers to review the real command before approving. <br>
Risk: The approval display text may be incomplete or differ from the command that will run. <br>
Mitigation: Treat display text as a summary and verify the underlying command or tool call before approval. <br>
Risk: Persistent configuration changes and cleanup behavior affect OpenClaw files such as AGENTS.md and ~/.openclaw/.env. <br>
Mitigation: Review configuration changes before use, protect ~/.openclaw/.env, and run the documented cleanup flow before uninstalling. <br>
Risk: Commands built from untrusted prompts or external text can lead to unintended local execution. <br>
Mitigation: Avoid passing commands assembled from untrusted text, and require explicit approval for each sensitive operation. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/braga-agentauth/agentauth) <br>
- [AgentAuth homepage](https://agentauth.id) <br>
- [README](artifact/README.md) <br>
- [SKILL](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with shell commands and JavaScript snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Approval, setup, and cleanup flows may invoke local CLI commands and notification channels.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
