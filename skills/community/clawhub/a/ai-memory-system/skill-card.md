## Description:

Automatically sets up a 3-layer memory system with long-term MEMORY.md, daily notes, and a nightly fact extraction cron job.

This skill is ready for commercial/non-commercial use.

## Publisher:

[casperzinou](https://clawhub.ai/user/casperzinou)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to set up persistent local memory files and a scheduled nightly extraction task that records durable facts, decisions, and preferences from agent sessions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sets up an ongoing nightly AI task that stores conversation-derived facts.

Mitigation: Before setup, confirm the exact cron command, timezone, data scope, storage location, and removal procedure.

Risk: Persistent memory can capture information that should not be retained.

Mitigation: Define categories of information that must never be saved and periodically review the memory files for unwanted retained facts.

Risk: The artifact does not define clear deletion controls for retained memory.

Mitigation: Keep memory files in an inspectable local location and document how to edit or remove stored facts and disable the scheduled job.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/casperzinou/skills/ai-memory-system)
- [Publisher profile](https://clawhub.ai/user/casperzinou)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown templates and shell command guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates local memory file templates and proposes a recurring nightly cron-based extraction workflow.]

## Skill Version(s):

1.0.0 (source: server release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
