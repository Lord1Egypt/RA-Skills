## Description: <br>
Use when the user wants to act on an audit, fix the findings in a line-check/bug-hunt/security-sweep report, work a prioritized backlog, or asks to "fix the findings", "work the backlog", "clear the audit", or "do the high-leverage items". <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[solomonneas](https://clawhub.ai/user/solomonneas) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to execute an existing audit backlog in leverage order, applying one focused fix at a time and verifying each finding before moving on. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill is intended to modify a repository, run verification, and make commits while resolving an audit backlog. <br>
Mitigation: Use it only for repositories where active audit-fix work is desired, keep changes isolated on a branch, and review the resulting commits before merging. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/solomonneas/expedite) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown status report with code changes, shell commands, verification notes, and commit references as applicable] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The skill may produce repository edits and commits when used to resolve audit findings.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
