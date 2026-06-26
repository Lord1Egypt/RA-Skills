## Description: <br>
Auto Revolution provides supervised workflow helpers for structured task files, review prompts, safety scanning, task state updates, and JSONL logging without bundled autonomous execution. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cjboy007](https://clawhub.ai/user/cjboy007) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to create and review structured task JSON, activate dependency-ready queued tasks, scan proposed instructions for risky shell patterns, apply review results, and maintain workflow logs under human supervision. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can reset task state, delete locks, and requeue work, which may disrupt workflow state if used on the wrong task or workspace. <br>
Mitigation: Install and run it only in a sandboxed project workspace, review task IDs and task JSON before use, and use force-unlock only after confirming the lock and recovery intent. <br>
Risk: Review prompts and generated next-step instructions can steer later work back into automatic agent processing with weaker safeguards than a fully supervised workflow. <br>
Mitigation: Keep a human in the loop for real execution, scan generated instructions before acting on them, and avoid automatic session or heartbeat workflows unless separately reviewed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/cjboy007/auto-revolution) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, JSON, markdown] <br>
**Output Format:** [Markdown guidance with command examples and JSON task or review artifacts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces supervised workflow instructions; bundled scripts can create or update local task files and append JSONL logs when run by the user.] <br>

## Skill Version(s): <br>
2.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
