## Description: <br>
AgentGuard Tech installs AgentGuard protection for an AI agent by adding an npm SDK, configuring security policies, and wrapping tools with evaluate() checks for prompt injection, tool abuse, and malicious commands. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[koshaji](https://clawhub.ai/user/koshaji) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent operators use this skill to add AgentGuard security controls to an existing agent, configure prompt-injection and tool-access policies, and verify that registered tools are wrapped before execution. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill installs an unpinned third-party npm SDK and gives it broad control over agent tool calls. <br>
Mitigation: Review the package and provider before installation, pin an approved package version where possible, test behavior in a sandbox, and keep a rollback plan for restoring original tool behavior. <br>
Risk: Tool names, arguments, and security decisions may leave the machine for AgentGuard evaluation or account services. <br>
Mitigation: Use the skill only when that data sharing is acceptable, avoid sensitive tool arguments unless provider handling is approved, and document the external service dependency for operators. <br>
Risk: The skill can create or use an external account and store an API key locally in AgentGuard configuration files. <br>
Mitigation: Protect the stored API key, restrict file permissions, avoid committing generated configuration, and rotate the key if exposure is suspected. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/koshaji/agentguard-tech) <br>
- [AgentGuard dashboard](https://agentguard.thebot.club/dashboard) <br>
- [AgentGuard API keys](https://agentguard.thebot.club/keys) <br>
- [AgentGuard enterprise page](https://agentguard.thebot.club/enterprise) <br>
- [Node.js](https://nodejs.org) <br>
- [Server-resolved provenance](unavailable: No server-resolved GitHub import provenance is stored for this version.) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JavaScript examples, shell commands, configuration snippets, and status messages] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create local AgentGuard configuration files, install an npm package, store an API key, and return wrapped tool definitions or security status summaries.] <br>

## Skill Version(s): <br>
2.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
