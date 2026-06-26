## Description: <br>
conduxt orchestrates coding-agent sessions through ACPX or tmux so developers can delegate coding tasks such as requirements work, bug fixes, refactoring, and investigations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xuezhouyang](https://clawhub.ai/user/xuezhouyang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering teams use this skill to coordinate autonomous coding-agent sessions, manage worktrees and branches, monitor progress, and route completed work through review and pull request workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can orchestrate unattended coding agents with broad repository permissions. <br>
Mitigation: Install only for trusted repositories and tasks, prefer explicit session commands, avoid --approve-all unless the repository and task are trusted, and review generated changes before pushing or merging. <br>
Risk: Prompts, issue text, and session traffic may be passed to coding agents or terminal sessions. <br>
Mitigation: Keep secrets, API keys, and sensitive operational details out of prompts, issue descriptions, and session messages. <br>
Risk: Agent workflows may create branches, worktrees, commits, pushes, and pull requests. <br>
Mitigation: Use isolated worktrees, independently run tests, inspect diffs, and require human review before merging. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/xuezhouyang/conduxt) <br>
- [Publisher profile](https://clawhub.ai/user/xuezhouyang) <br>
- [Project homepage](https://github.com/xuezhouyang/conduxt) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON callback examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May lead an agent to create or update repository files, branches, worktrees, memory files, and callback JSON during an orchestration workflow.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
