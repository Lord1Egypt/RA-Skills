## Description: <br>
Claude Swarm orchestrates multiple Claude Code agents for parallel coding with git worktrees, tmux tracking, endorsement gates, auto-review chains, integration merging, and notifications. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[linkbag](https://clawhub.ai/user/linkbag) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering teams use this skill to coordinate multiple Claude Code agents across parallel implementation, review, and integration tasks in a git repository. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can run background Claude Code agents with broad permission settings that modify repository files, create commits, push branches, and open pull requests. <br>
Mitigation: Run it only in repositories where autonomous code changes are intended; prefer forks or disposable branches, review all diffs before merging, and monitor or stop tmux sessions as needed. <br>
Risk: Batch and watcher scripts can install dependencies and perform automated review or integration steps with active git, GitHub, and Claude credentials. <br>
Mitigation: Verify credentials and configuration before use, disable auto-merge behavior unless explicitly wanted, and avoid unattended execution in sensitive repositories. <br>
Risk: Optional webhook or Telegram notifications can send workflow status outside the local environment. <br>
Mitigation: Leave notifications disabled unless needed, and only configure notification endpoints approved for the repository and team. <br>


## Reference(s): <br>
- [Claude Swarm on ClawHub](https://clawhub.ai/linkbag/claude-swarm) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and script-driven repository changes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create worktrees, branches, commits, pull requests, logs, and notification messages through the bundled shell scripts.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
