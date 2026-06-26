## Description: <br>
Applies approved improvement candidates to target files, supports rollback and dry-run previews, and handles append, replace, insert-before, and YAML frontmatter update actions with automatic backups. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lanyasheng](https://clawhub.ai/user/lanyasheng) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to apply accepted low-risk improvement candidates to documentation, reference, or guardrail files and to roll back prior executions from receipts or backups. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can modify local files when executing accepted candidates. <br>
Mitigation: Run it on a disposable branch or backed-up workspace and review the candidate action, target path, and generated diff before keeping changes. <br>
Risk: The force option can bypass the normal recommendation check. <br>
Mitigation: Use force only after explicit human approval and keep unsupported or higher-risk categories routed through the gate workflow. <br>
Risk: Rollback depends on valid receipts, backup paths, and target paths. <br>
Mitigation: Preserve execution artifacts and backup directories, and test rollback with dry-run before executing restoration. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/lanyasheng/auto-improvement-executor) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [JSON execution and rollback artifacts with diffs, status fields, trace metadata, and shell command usage guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May modify local files, create backups, emit rollback pointers, and return dry-run or unsupported statuses depending on candidate recommendation, category, action, and rollback inputs.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
