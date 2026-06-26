## Description: <br>
Process multiple items with progress tracking, checkpointing, and failure recovery. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ivangdavila](https://clawhub.ai/user/ivangdavila) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agents use this skill to plan and run batch work with dry runs, progress updates, checkpoints, retry handling, and recovery paths for partial failures. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Large batches or destructive operations can amplify mistakes across many items. <br>
Mitigation: Use dry runs and item counts before execution, require explicit confirmation for deletes or modifications, and keep rollback backups until results are verified. <br>
Risk: Checkpoint, backup, rollback, or failed-item files may contain private data. <br>
Mitigation: Clean up these files after verification and handle them as sensitive artifacts while they exist. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ivangdavila/batch) <br>
- [Batch Error Handling](artifact/errors.md) <br>
- [Batch Strategies](artifact/strategies.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, shell commands] <br>
**Output Format:** [Markdown guidance with progress summaries, retry patterns, and checkpoint or rollback examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce checkpoint, backup, failed-item, or rollback files when the agent applies the guidance to a batch task.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
