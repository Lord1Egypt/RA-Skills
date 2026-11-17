## Description:

Structured memory system for OpenClaw agents that sets up long-term memory files, feedback capture, topic notes, and heartbeat maintenance rules.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kaiji-z](https://clawhub.ai/user/kaiji-z)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use Claude Memory to initialize and maintain a local long-term memory structure for OpenClaw agents, including feedback, daily notes, and topic files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill is designed to create persistent local memory files that may retain personal, regulated, or confidential information if users choose to save it.

Mitigation: Review MEMORY.md, memory/feedback.md, and daily notes periodically, and avoid saving sensitive information unless retention is intentional.

## Reference(s):

- [AGENTS.md Memory Rules](references/agents-rules.md)
- [Encoding Notes](references/encoding-notes.md)
- [ClawHub Skill Page](https://clawhub.ai/kaiji-z/skills/claude-memory)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands and Python setup script output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates local MEMORY.md, memory/feedback.md, daily notes, and memory/topics files when the setup script is run.]

## Skill Version(s):

1.2.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
