## Description: <br>
Coordinates multiple AI agents in isolated git worktrees for code development, testing, and review. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[liuchang8877](https://clawhub.ai/user/liuchang8877) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering teams use this skill to coordinate coder, tester, and reviewer agents across isolated git worktrees during multi-phase code changes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Example git worktree and codex commands can create local branches, write files, and change directories if run as shown. <br>
Mitigation: Replace the example paths, run commands only from the intended repository, and confirm the working tree is recoverable before use. <br>
Risk: Agent-produced code or review guidance may be incorrect or unsuitable for merging. <br>
Mitigation: Review all agent-produced diffs and reviewer feedback before accepting or merging changes. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/liuchang8877/agent-team-pipeline) <br>
- [Publisher profile](https://clawhub.ai/user/liuchang8877) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline bash code blocks and workflow tables] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces workflow instructions for agent coordination; does not execute commands unless a user runs the examples.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
