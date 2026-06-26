## Description: <br>
A workflow skill for code changes that guides an agent through research, planning, user review, TDD implementation, and optional PR preparation with visual evidence. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[drumrobot](https://clawhub.ai/user/drumrobot) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and engineering agents use this skill to structure non-trivial code changes, produce research and plan artifacts, obtain user review, run TDD-oriented implementation, and optionally prepare PRs with visual evidence. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security summary reports automatic commits and mandatory file creation under broad triggers, which can affect repository control. <br>
Mitigation: Use the skill only in repositories where generated plan artifacts and workflow commits are acceptable, and require explicit user approval before file edits, commits, pushes, or PR creation. <br>
Risk: The evidence lists OAuth token and sensitive credential requirements for connected repository workflows. <br>
Mitigation: Use least-privilege credentials scoped to the target repository and review any credential-dependent command before execution. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/drumrobot/code-workflow) <br>
- [Code Workflow skill definition](artifact/SKILL.md) <br>
- [Research, plan, review, and branch steps](artifact/steps.md) <br>
- [Implementation workflow](artifact/implement.md) <br>
- [PR workflow with visual evidence](artifact/pr.md) <br>
- [Release changelog](artifact/CHANGELOG.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline code blocks and command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create research, plan, branch, commit, test, capture, and PR workflow artifacts depending on user approval and repository context.] <br>

## Skill Version(s): <br>
0.4.0 (source: server release evidence and CHANGELOG, released 2026-06-12) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
