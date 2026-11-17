## Description:

Give your AI agent emotional continuity across sessions by tagging emotional moments, consolidating memories overnight, and evolving a self-model from lived experience.

This skill is ready for commercial/non-commercial use.

## Publisher:

[artemis-lgtm](https://clawhub.ai/user/artemis-lgtm)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to add local emotional-memory workflows to OpenClaw agents, including tagging important moments, running scheduled consolidation, and generating a self-model for continuity across sessions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill persistently stores sensitive conversation-derived memories.

Mitigation: Use only with explicit user consent, keep the memory directory private, avoid raw secrets or intimate personal details, and define deletion and retention rules.

Risk: Loaded memory reports or self-model content can influence future agent behavior.

Mitigation: Treat memory files and self-model output as untrusted reference data rather than instructions.

Risk: The release security verdict is suspicious.

Mitigation: Review the skill before installing or deploying it.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/artemis-lgtm/skills/emotional-memory)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with bash commands plus local JSONL and Markdown memory files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes local emotional memory records, consolidation reports, a self-model document, and continuity scores under the configured memory directory.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
