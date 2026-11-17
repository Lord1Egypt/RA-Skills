## Description:

Task Tracker maintains a compact task state file so agents can track active work, background processes, progress, completion, and failure across session resets.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rikouu](https://clawhub.ai/user/rikouu)

### License/Terms of Use:


## Use Case:

Agents and their operators use this skill to maintain a compact memory/tasks.md state snapshot for active work, background processes, and recent completed tasks so work can resume after compaction or session resets.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent task notes may capture sensitive commands, links, server names, or confidential task outputs.

Mitigation: Use the skill only where persistent task tracking is acceptable, and redact secrets, private commands, authenticated links, sensitive server names, and confidential outputs before storing task state.

Risk: Automatic write-first tracking can preserve more operational detail than a user expects across session resets.

Mitigation: Review memory/tasks.md regularly, keep entries concise, compress completed work, and prune stale completed tasks as described by the artifact.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/rikouu/skills/agent-task-tracker)

## Skill Output:

**Output Type(s):** [markdown, configuration, guidance]

**Output Format:** [Markdown task-state snapshot in memory/tasks.md]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Keeps active task state under 50 lines / 2KB and compresses recent completed tasks to one-line summaries.]

## Skill Version(s):

1.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
