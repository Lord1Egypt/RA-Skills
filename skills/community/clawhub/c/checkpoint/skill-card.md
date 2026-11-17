## Description:

Part of the Overpowered skill suite, this skill helps an agent create a durable, self-contained state package so a fresh agent, session, or different harness can resume non-trivial work without the original chat history.

This skill is ready for commercial/non-commercial use.

## Publisher:

[raguets](https://clawhub.ai/user/raguets)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill during long-running work, context resets, handoffs, or pauses to preserve enough state for another capable agent to resume without the original chat transcript. It is not intended for trivial finished tasks where a checkpoint would add little value.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A checkpoint may preserve secrets, private transcript details, or unnecessary confidential project material.

Mitigation: Specify the destination for sensitive projects and review the checkpoint before retaining or sharing it.

## Reference(s):

- [Overpowered skill suite](https://github.com/raguets/overpowered)
- [ClawHub checkpoint skill](https://clawhub.ai/raguets/skills/checkpoint)

## Skill Output:

**Output Type(s):** [markdown, guidance]

**Output Format:** [Markdown checkpoint file]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates or updates CHECKPOINT.md in the working directory unless the user specifies another destination.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
