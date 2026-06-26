## Description: <br>
Manage Coder workspaces and AI coding agent tasks via CLI. List, create, start, stop, and delete workspaces. SSH into workspaces to run commands. Create and monitor AI coding tasks with Claude Code, Aider, or other agents. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[DevelopmentCats](https://clawhub.ai/user/DevelopmentCats) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and engineers use this skill to operate Coder workspaces and Coder Tasks from an OpenClaw agent, including workspace lifecycle actions, remote command execution, and AI coding task management. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A Coder session token can grant access to workspace and task operations if exposed. <br>
Mitigation: Keep CODER_SESSION_TOKEN out of commits, logs, screenshots, and shared prompts; prefer least-privilege or short-lived tokens where available and rotate or revoke the token if it is exposed. <br>
Risk: Workspace deletion, task deletion, restarts, or broad remote commands can disrupt active development work. <br>
Mitigation: Require explicit confirmation before destructive workspace or task operations and before broad remote command execution. <br>


## Reference(s): <br>
- [Coder Docs](https://coder.com/docs) <br>
- [Coder CLI Docs](https://coder.com/docs/install/cli) <br>
- [Coder Tasks Docs](https://coder.com/docs/ai-coder) <br>
- [ClawHub Skill Page](https://clawhub.ai/DevelopmentCats/coder-workspaces) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration instructions] <br>
**Output Format:** [Markdown with inline shell commands and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the coder CLI plus CODER_URL and CODER_SESSION_TOKEN in the agent environment.] <br>

## Skill Version(s): <br>
1.5.5 (source: changelog and server release metadata, released 2026-02-06) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
