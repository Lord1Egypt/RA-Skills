## Description: <br>
Coding Swarm Agent coordinates tmux-driven Claude Code and Codex agents for delegated coding, writing, analysis, review, testing, image, and deployment workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ayao99315](https://clawhub.ai/user/ayao99315) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering teams use this skill to decompose complex project work, dispatch scoped tasks to coding agents, monitor task status, cross-review outputs, and coordinate commits or deployments in a local ClawHub/OpenClaw workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can grant agents broad authority to commit, push, install persistent hooks, send notifications, and run deployment commands. <br>
Mitigation: Install only in an isolated, trusted repository and enable automatic commit, push, hook, notification, and deployment paths only after review. <br>
Risk: Bypass-sandbox or highly automated command paths can execute project-changing operations with limited human intervention. <br>
Mitigation: Review and disable bypass-sandbox command examples unless that level of automation is explicitly intended for the repository. <br>
Risk: Delegated coding agents can produce incorrect or out-of-scope changes that are then committed or deployed. <br>
Mitigation: Use file-scoped task prompts, cross-review agent outputs, inspect commit diffs, and run the release dashboard before deployment. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/ayao99315/ayao-workflow-agent) <br>
- [Agent Swarm Playbook](references/agent-swarm-playbook.md) <br>
- [Task Schema](references/task-schema.md) <br>
- [Cross-Review Prompt Template](references/prompt-cc-review.md) <br>
- [Codex Backend Coding Prompt Template](references/prompt-codex.md) <br>
- [Codex Deploy Prompt Template](references/prompt-codex-deploy.md) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Code, Shell commands, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands, prompt templates, JSON task records, and code change instructions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May coordinate task registry updates, git commits, pushes, hooks, notifications, and deployment commands through delegated agents.] <br>

## Skill Version(s): <br>
1.7.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
