## Description:

Manage and optimize OpenClaw context window usage via partitioning, pre-compression checkpointing, and information lifecycle management.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sarielwang93](https://clawhub.ai/user/sarielwang93)

### License/Terms of Use:


## Use Case:

Developers and agent operators use this skill to manage long-running OpenClaw sessions by partitioning context, checkpointing important state before compaction, and reducing the risk of losing task progress.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent checkpoint memory could preserve copied commands, policy changes, credentials, or untrusted instructions.

Mitigation: Review or constrain HOT_MEMORY.md updates so checkpoints contain only factual task state before relying on the skill.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes checkpointing guidance and a helper shell script for OpenClaw context cleanup.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
