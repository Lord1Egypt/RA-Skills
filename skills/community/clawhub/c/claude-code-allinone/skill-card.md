## Description: <br>
Installs, configures, and runs Claude Code CLI inside ArkClaw/OpenClaw sandboxes with review and build routing for AgentPlan, Coding Plan, or a custom Anthropic-compatible gateway. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bao2200220](https://clawhub.ai/user/bao2200220) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers working in ArkClaw/OpenClaw use this skill to set up Claude Code CLI, route coding requests into read-only review or file-editing build mode, and switch among supported model provider profiles. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill stores sensitive API keys and Claude configuration in local home-directory files. <br>
Mitigation: Install only when comfortable with local credential storage, review generated configuration, and remove stored keys and profile files when the skill is no longer used. <br>
Risk: Build mode can run a shell-capable coding agent that edits files with limited confirmation. <br>
Mitigation: Prefer review mode for analysis, inspect proposed changes before relying on them, and run the skill only in workspaces where file edits and shell commands are acceptable. <br>
Risk: Incorrect provider, model, or key selection can cause authentication failures or route requests to an unintended compatible gateway. <br>
Mitigation: Use the health check and provider references before switching profiles, and confirm the active provider when troubleshooting authentication or routing errors. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/bao2200220/claude-code-allinone) <br>
- [Provider reference](references/providers.md) <br>
- [Routing flow reference](references/routing-flow.md) <br>
- [Troubleshooting reference](references/troubleshooting.md) <br>
- [Volcengine](https://www.volcengine.com/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown and terminal-style text with shell commands, configuration actions, and Claude Code output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can run Claude Code in read-only review mode or build mode with Read, Glob, Grep, LS, Bash, Edit, and Write tools; run logs are retained locally.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
