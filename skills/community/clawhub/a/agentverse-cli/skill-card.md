## Description: <br>
Publish, discover, and manage AI skills, agents, workflows, souls and prompts from the AgentVerse marketplace. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[loonghao](https://clawhub.ai/user/loonghao) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and AI agents use this skill to discover, publish, authenticate, and manage AgentVerse marketplace artifacts through the agentverse CLI. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Installer scripts and self-update commands can execute downloaded code. <br>
Mitigation: Use verified release binaries when available, inspect installer scripts before running them, and require explicit approval before install or self-update commands. <br>
Risk: Saved credentials and tokens such as AGENTVERSE_TOKEN or GitHub tokens can authorize account actions. <br>
Mitigation: Protect tokens, avoid logging them, prefer least-privilege credentials, and clear or rotate credentials when no longer needed. <br>
Risk: Publish, update, deprecate, comment, rate, learn, benchmark, login, and self-update commands can change public marketplace or account state. <br>
Mitigation: Require explicit user approval, review command targets and payloads, and confirm the active server before executing state-changing commands. <br>


## Reference(s): <br>
- [AgentVerse repository](https://github.com/loonghao/agentverse) <br>
- [AgentVerse API documentation](https://github.com/loonghao/agentverse#api-documentation) <br>
- [ClawHub release page](https://clawhub.ai/loonghao/agentverse-cli) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and CLI examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include commands that authenticate, publish, mutate marketplace state, or self-update; require explicit approval before execution.] <br>

## Skill Version(s): <br>
0.1.4 (source: server release metadata, target metadata, SKILL.md frontmatter, skill.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
