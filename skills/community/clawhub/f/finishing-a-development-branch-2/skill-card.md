## Description: <br>
Use when implementation is complete, all tests pass, and you need to decide how to integrate the work - guides completion of development work by presenting structured options for merge, PR, or cleanup. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lovemymobilewebsite-dotcom](https://clawhub.ai/user/lovemymobilewebsite-dotcom) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering agents use this skill after implementation work is complete to verify tests, choose a branch completion path, and perform merge, pull request, branch retention, or discard cleanup steps. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The PR workflow may remove a local worktree despite the release evidence warning about inconsistent cleanup instructions. <br>
Mitigation: Before choosing the PR path, explicitly tell the agent whether the worktree must be preserved and verify the final cleanup plan before it runs worktree removal commands. <br>
Risk: Branch completion actions can push code, create pull requests, merge changes, or delete local work. <br>
Mitigation: Review the target remote, GitHub account, branch contents, sensitive files, and test results before allowing push, PR, merge, or discard steps. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/lovemymobilewebsite-dotcom/finishing-a-development-branch-2) <br>
- [Publisher profile](https://clawhub.ai/user/lovemymobilewebsite-dotcom) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Markdown] <br>
**Output Format:** [Markdown with inline shell commands and structured option prompts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the agent to verify tests before integration and to request explicit confirmation before discarding work.] <br>

## Skill Version(s): <br>
0.1.0 (source: release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
