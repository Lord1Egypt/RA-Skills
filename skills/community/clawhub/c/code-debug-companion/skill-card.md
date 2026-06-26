## Description: <br>
AI-powered code debugging assistant that diagnoses errors, researches related solutions, proposes or writes fixes, and validates them with tests. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zlszhonglongshen](https://clawhub.ai/user/zlszhonglongshen) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers use this skill to triage pasted errors, screenshots, logs, or stack traces; identify likely root causes; research related solutions; and generate fixes with test coverage. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may modify project files while debugging. <br>
Mitigation: Use it in a version-controlled workspace and review diffs before accepting edits. <br>
Risk: The skill may search externally using error text or stack traces. <br>
Mitigation: Remove secrets and proprietary details before allowing external search. <br>
Risk: The skill may create GitHub issues as part of its workflow. <br>
Mitigation: Require confirmation before any issue is created or published. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zlszhonglongshen/code-debug-companion) <br>
- [Publisher profile](https://clawhub.ai/user/zlszhonglongshen) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, guidance] <br>
**Output Format:** [Structured Markdown report with diagnosis, related findings, fix details, test coverage, and changed files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include proposed or applied file changes and generated unit tests when the agent is permitted to edit the workspace.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence and workflow.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
