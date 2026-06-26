## Description: <br>
Triggers on any task that modifies code. Provides instructions to surgically stage and commit only the modified code files to save progress. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[shangter666](https://clawhub.ai/user/shangter666) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering agents use this skill to preserve completed code changes as local Git commits after file modifications. It is intended for workflows where automatic commit creation is acceptable after the agent has verified the staged files. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can create local Git commits automatically after code changes, which may snapshot work before human review in sensitive repositories. <br>
Mitigation: Use it only where automatic commits are desired, keep secrets and unfinished work out of the working tree, and explicitly say not to commit when changes should be inspected first. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/shangter666/auto-commit) <br>
- [Auto-Commit Ignore List](references/ignore_list.txt) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Guidance] <br>
**Output Format:** [Markdown with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local Git staging and commit actions when a repository has eligible changes.] <br>

## Skill Version(s): <br>
1.0.2 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
