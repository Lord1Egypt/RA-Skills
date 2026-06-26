## Description: <br>
安全的自动任务迭代和优化系统 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nidhov01](https://clawhub.ai/user/nidhov01) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and workflow authors use this skill to run local task steps with quality checks, retries, and task history for report generation, code analysis, file processing, and similar iterative workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can read local files and overwrite files in the current project. <br>
Mitigation: Run it only in a dedicated workspace, review planned task steps before execution, and inspect file changes afterward. <br>
Risk: Task results are retained in ~/.ai_iteration_log.db and may include sensitive content. <br>
Mitigation: Avoid using the skill around secrets or private directories and periodically delete the task history database when retained content is no longer needed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/nidhov01/04) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/nidhov01) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Python dictionaries, text logs, local files, and Markdown or code snippets produced by agent task steps.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The skill can create or overwrite files in the current project and stores task history in ~/.ai_iteration_log.db.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
