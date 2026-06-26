## Description: <br>
Orchestrates Cursor Agent CLI coding workflows with concurrency control, timeout recovery, and multi-step coordination. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[slk1061569042-lab](https://clawhub.ai/user/slk1061569042-lab) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineering agents use this skill to plan, execute, monitor, and recover Cursor Agent CLI coding tasks, including parallel batches and plan-then-execute workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide an agent to auto-edit code, create commits, and run background Cursor Agent jobs. <br>
Mitigation: Start in plan or ask mode, review the proposed diff before using --yolo, and require explicit user approval before commits. <br>
Risk: Cleanup guidance includes process-kill commands that could stop unrelated Cursor Agent jobs. <br>
Mitigation: Inspect active processes first and avoid broad pkill cleanup unless unrelated Cursor Agent work has been ruled out. <br>
Risk: Parallel execution can create file or git conflicts when tasks touch overlapping code. <br>
Mitigation: Keep execute tasks serial for the same file, limit write-mode concurrency, and verify the worktree and tests after each batch. <br>


## Reference(s): <br>
- [Cursor Dispatch on ClawHub](https://clawhub.ai/slk1061569042-lab/cursor-dispatch) <br>
- [slk1061569042-lab Publisher Profile](https://clawhub.ai/user/slk1061569042-lab) <br>
- [Models and Parameters Reference](references/models-and-params.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, guidance] <br>
**Output Format:** [Markdown guidance with inline shell command templates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include Cursor CLI flags, concurrency limits, timeout values, and recovery steps.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
