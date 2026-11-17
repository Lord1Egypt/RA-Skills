## Description: <br>
批处理专家 helps agents plan and execute batch-processing workflows with dry runs, streaming chunks, checkpoints, idempotency, progress reporting, and error handling. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thcjp](https://clawhub.ai/user/thcjp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to design safer batch jobs for large file sets, API workloads, media conversion, and data-cleaning tasks. It focuses on avoiding out-of-memory failures, recovering interrupted runs, preventing duplicate work, and making progress visible. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Batch operations can affect many files, records, messages, payments, accounts, or production data at once. <br>
Mitigation: Require a small dry run, review the exact command or script, and explicitly confirm destructive or irreversible operations before running the full batch. <br>
Risk: Interrupted or retried batch jobs can lose progress or duplicate work. <br>
Mitigation: Use persistent checkpoints, idempotency keys, retry limits, and a confirmed rollback or retry plan before processing production data. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/thcjp/skills/batch-processor-pro) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with code snippets, command proposals, and checklist-style recommendations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Emphasizes dry runs, checkpoints, idempotency, progress reporting, and review of destructive operations before execution.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
