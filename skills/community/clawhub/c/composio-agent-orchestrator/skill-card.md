## Description: <br>
Open-source, pluggable coding-agent orchestrator that helps agents spawn, monitor, and manage durable coding sessions for bugs, features, GitHub issues, pull request feedback, and CI follow-up. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[illegalcall](https://clawhub.ai/user/illegalcall) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to coordinate coding work through AO, including spawning isolated agent sessions, checking progress, routing review or CI feedback, and cleaning up sessions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Approved AO sessions can work in repositories and use the GitHub credentials available through gh. <br>
Mitigation: Use least-privilege GitHub credentials scoped to the repositories AO needs, and review each proposed spawn or batch spawn before approving it. <br>
Risk: Agent worktrees and running sessions can expose local secrets if credentials or environment files are copied into those workspaces. <br>
Mitigation: Keep secrets out of agent worktrees, avoid symlinking sensitive files, and use a dedicated Anthropic API key with spending limits. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/illegalcall/composio-agent-orchestrator) <br>
- [Agent Orchestrator config reference](references/config.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guidance may include AO session status, PR URLs returned by AO tools, setup commands, and YAML configuration examples.] <br>

## Skill Version(s): <br>
1.0.5 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
