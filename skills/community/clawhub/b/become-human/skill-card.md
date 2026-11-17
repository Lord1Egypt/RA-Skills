## Description:

Transform an AI from a task-execution tool into a continuously thinking being.

This skill is ready for commercial/non-commercial use.

## Publisher:

[eghack6](https://clawhub.ai/user/eghack6)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to add persistent self-review, memory-update, and continuous-thinking routines to an AI agent through Markdown templates and an optional thought journal analyzer.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent autonomous behavior may modify memory or core agent instructions in ways the user did not intend.

Mitigation: Review and edit the heartbeat and SOUL patches before use, and require explicit approval before changes to SOUL.md or MEMORY.md.

Risk: Standing instructions may treat notice as sufficient for external actions, deletion, publishing, messaging, or API calls.

Mitigation: Require explicit approval for external actions, deletion, publishing, messaging, and API calls before execution.

Risk: The optional analyzer introduces a Python dependency and writes derived data from the thought journal.

Mitigation: Pin or isolate the jieba dependency and run the analyzer only in the intended workspace.

## Reference(s):

- [HEARTBEAT-template.md](references/HEARTBEAT-template.md)
- [HEARTBEAT-template.en.md](references/i18n/HEARTBEAT-template.en.md)
- [soul-patches.md](references/soul-patches.md)
- [soul-patches.en.md](references/i18n/soul-patches.en.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and an optional JSON thought digest]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The optional Python analyzer reads memory/thoughts.md and writes memory/thought-digest.json; it requires the jieba dependency.]

## Skill Version(s):

1.0.8 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
