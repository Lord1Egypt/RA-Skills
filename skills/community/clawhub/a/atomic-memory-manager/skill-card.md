## Description:

Recall and write workspace memory for OpenClaw agents using MEMORY.md, memory/YYYY-MM-DD.md, memory_search, and memory_get.

This skill is ready for commercial/non-commercial use.

## Publisher:

[omaression](https://clawhub.ai/user/omaression)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to retrieve prior workspace decisions, preferences, todos, and durable notes, and to write concise memory entries when information should persist across sessions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent memory can carry sensitive or outdated information into later sessions.

Mitigation: Avoid storing secrets, keep notes limited to durable facts, and flag stale memory when it affects an answer.

Risk: Weak memory retrieval can produce misleading answers if prior context is guessed.

Mitigation: Retrieve focused snippets first, answer from retrieved text, and state when memory results are weak or unavailable.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/omaression/skills/atomic-memory-manager)
- [Publisher profile](https://clawhub.ai/user/omaression)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown or plain text guidance with memory file references when useful]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May cite retrieved memory file paths and lines when answering from stored context.]

## Skill Version(s):

1.0.0-alpha (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
