## Description: <br>
A persistent local-only memory system for AI coding agents that uses a committed AGENTS.md file and a gitignored .agents.local.md scratchpad to carry project context across sessions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[AndreaGriffiths11](https://clawhub.ai/user/AndreaGriffiths11) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and engineering teams use this skill to set up shared, reviewable agent context for coding projects and personal session memory that can be promoted into project guidance over time. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The setup can persistently change agent instructions through AGENTS.md and .agents.local.md. <br>
Mitigation: Review proposed AGENTS.md and scratchpad changes like normal code, keep secrets and untrusted instructions out of .agents.local.md, and require user approval before session notes are written. <br>
Risk: The publish workflow can push an entire workspace to GitHub. <br>
Mitigation: Do not run the publish script until git status and the files staged for publication have been checked, and avoid publishing sensitive or unintended project files. <br>
Risk: The security summary reports a missing CLI dependency for setup behavior. <br>
Mitigation: Confirm the expected agent-context CLI or wrapper exists before running setup, and inspect shell scripts before execution. <br>
Risk: Autopromotion can move scratchpad content into shared project guidance without enough review. <br>
Mitigation: Avoid --autopromote unless the proposed AGENTS.md additions have been reviewed and are appropriate for all project agents. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/AndreaGriffiths11/agent-context-system) <br>
- [README.md](README.md) <br>
- [AGENTS.md template](AGENTS.md) <br>
- [Architecture reference](agent_docs/architecture.md) <br>
- [Conventions reference](agent_docs/conventions.md) <br>
- [Gotchas reference](agent_docs/gotchas.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and configuration file changes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local project context files and agent configuration guidance; no external service output is required.] <br>

## Skill Version(s): <br>
1.3.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
