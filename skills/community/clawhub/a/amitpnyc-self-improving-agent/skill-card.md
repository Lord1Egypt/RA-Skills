## Description:

Log high-signal corrections, tool failures, feature requests, and recurring workflow lessons to a lightweight .learnings/ directory, then promote only repeated or durable learnings into durable instruction or memory files for OpenClaw or coding-agent workspaces that should improve over time without accumulating noise.

This skill is ready for commercial/non-commercial use.

## Publisher:

[amitpnyc](https://clawhub.ai/user/amitpnyc)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and coding-agent users use this skill to capture high-value lessons from corrections, tool failures, feature requests, and recurring workflow issues. It helps teams keep lightweight append-only learning logs and promote only durable lessons into higher-authority instruction or memory files after review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent learning logs may retain sensitive workspace details if an agent records too much context.

Mitigation: Record short sanitized summaries, redact sensitive excerpts, and do not log secrets, tokens, private keys, environment variables, raw customer data, or full sensitive transcripts unless explicitly requested.

Risk: Promoting lessons into AGENTS.md, MEMORY.md, SOUL.md, TOOLS.md, or project instructions can influence future agent behavior.

Mitigation: Review and explicitly authorize proposed promotion into durable instruction or memory files before accepting the change.

Risk: Low-signal or duplicate entries can create noisy learning history that is harder to maintain.

Mitigation: Use the skill's logging threshold, recurrence metadata, and deduplication guidance before appending new entries or promoting lessons.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/amitpnyc/skills/amitpnyc-self-improving-agent)

## Skill Output:

**Output Type(s):** [text, markdown, files, guidance]

**Output Format:** [Markdown log entries and concise guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Append-only .learnings entries by default; durable instruction or memory edits only after review or explicit authorization.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
