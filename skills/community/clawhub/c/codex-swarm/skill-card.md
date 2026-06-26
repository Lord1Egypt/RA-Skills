## Description: <br>
Codex Swarm orchestrates multiple OpenAI Codex CLI agents for parallel coding with git worktrees, tmux tracking, endorsement gates, code review, integration merging, and notifications. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[linkbag](https://clawhub.ai/user/linkbag) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to coordinate parallel Codex coding tasks across isolated git worktrees, review branches, and integrate completed work. It is intended for repositories where the operator deliberately wants automated agents to create branches, commits, pull requests, and optional merges. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can run background Codex agents that commit, push, and merge repository changes. <br>
Mitigation: Use a fork or protected branches, disable auto-merge unless explicitly needed, and review diffs before changes reach main. <br>
Risk: Task prompts and completion notices can flow through local logs or optional external notification endpoints. <br>
Mitigation: Avoid sensitive task prompts and enable external notifications only with trusted endpoints. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/linkbag/codex-swarm) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline bash commands and JSON configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires local repository access and CLI tooling such as bash, tmux, git, gh, jq, and Codex CLI.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
