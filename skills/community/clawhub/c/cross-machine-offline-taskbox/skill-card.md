## Description:

Helps agents queue, exchange, and process tasks across machines with a local offline taskbox and an Ollama worker.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhaoxinghua09-cell](https://clawhub.ai/user/zhaoxinghua09-cell)

### License/Terms of Use:

MIT (Python code); All rights reserved (documentation and theory)

## Use Case:

Developers and agent users can manage local task queues, transfer tasks between machines, and process queued work with a locally installed Ollama model when offline.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Task data is stored beside the skill and may contain sensitive content.

Mitigation: Keep task data and exchanged sync packs on trusted local machines.

Risk: The worker runs a local Ollama executable and model.

Mitigation: Verify the executable and model are trusted before processing tasks.

Risk: Deleting a task does not ask for confirmation.

Mitigation: Check task IDs before deletion and retain a sync pack when recovery matters.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/zhaoxinghua09-cell/skills/cross-machine-offline-taskbox)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Text]

**Output Format:** [Markdown guidance and command-line text; local JSON task records and sync packs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Local worker responses are written back to task records.]

## Skill Version(s):

2.2.5 (source: server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
