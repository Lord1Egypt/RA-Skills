## Description: <br>
Helps agents plan, split, checkpoint, monitor, and recover complex multi-step or batch tasks while managing sub-agent timeouts, context growth, and concurrent write risks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xwz119](https://clawhub.ai/user/xwz119) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to orchestrate long-running or high-volume work, choose serial, parallel, checkpointed, or hybrid execution patterns, and recover cleanly after failures or context loss. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill intentionally writes task logs and checkpoint files, which may capture sensitive prompts, credentials, document tokens, file paths, or confidential content if used carelessly. <br>
Mitigation: Avoid recording secrets or confidential data in logs, keep checkpoints scoped to operational status, and periodically review or delete generated logs. <br>
Risk: Concurrent writes to shared files, documents, or APIs can cause conflicts, overwritten results, or partial outputs. <br>
Mitigation: Use a single writer, give sub-agents separate output files, prefer incremental append or insert operations, and merge results in the main session. <br>


## Reference(s): <br>
- [Common Task Orchestration Patterns](artifact/references/common-patterns.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/xwz119/complex-task-orchestrator) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance with optional code blocks, command examples, JSON checkpoint structures, and progress reporting templates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce persistent task logs and checkpoint files for recovery.] <br>

## Skill Version(s): <br>
1.2.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
