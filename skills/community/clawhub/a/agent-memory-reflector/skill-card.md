## Description:

Enables AI agents to review past decisions, identify reasoning loops, and produce self-improvement insights.

This skill is ready for commercial/non-commercial use.

## Publisher:

[albionaiinc-del](https://clawhub.ai/user/albionaiinc-del)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent builders use this skill to log agent prompts, responses, and metadata, then generate reflection reports that highlight repeated queries, uncertainty patterns, and self-correction trends.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can persist full prompts, responses, metadata, and retrieved context in plaintext local files.

Mitigation: Do not log secrets, credentials, personal data, proprietary code, or sensitive retrieved context unless local plaintext storage is acceptable.

Risk: Memory files have weak scoping and no built-in retention or privacy controls.

Mitigation: Use separate working directories per agent and periodically delete .agent_memory when the retained history is no longer needed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/albionaiinc-del/skills/agent-memory-reflector)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, guidance]

**Output Format:** [Command-line text output and local JSONL records]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Stores interaction and reflection records locally in .agent_memory JSONL files.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
