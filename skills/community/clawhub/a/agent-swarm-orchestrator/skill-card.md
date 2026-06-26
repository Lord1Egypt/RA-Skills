## Description: <br>
Orchestrates OpenClaw Agent Swarm workflows for multi-project coding automation with Obsidian task intake, Claude coding, Codex review, GitLab merge request flow, merge and sync, and done-status closure. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Matzoh](https://clawhub.ai/user/Matzoh) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineering teams use this skill to coordinate local multi-project coding automation: intake tasks from Obsidian, spawn coding-agent worktrees, run review, create merge requests, sync merged work, and close task state. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can autonomously edit repositories, push branches, create or merge merge requests, and clean up local worktrees. <br>
Mitigation: Use dedicated low-privilege Git and AI accounts, start with test repositories, and add confirmation gates for repo creation, pushes, merges, and cleanup. <br>
Risk: The automation reads local repositories, Obsidian task notes, AI-tool sessions, Git provider credentials, and notification destinations. <br>
Mitigation: Keep the Obsidian intake folder controlled, restrict credential scope, and run the skill only in workspaces intended for autonomous coding infrastructure. <br>
Risk: Cron-driven monitors and notification scripts can continue acting after initial setup. <br>
Mitigation: Review cron entries before enabling them, monitor generated task state and logs, and require confirmation for external notifications where appropriate. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/Matzoh/agent-swarm-orchestrator) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance, Markdown] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May trigger local scripts that create worktrees, run agent sessions, push branches, create or merge merge requests, update task state, and send notifications.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
