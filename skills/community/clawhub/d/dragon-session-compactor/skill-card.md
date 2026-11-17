## Description:

Compacts long agent chat sessions into local summaries while preserving the most recent messages.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xhmqq616](https://clawhub.ai/user/xhmqq616)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to keep long OpenClaw-style conversations within context limits by checking session size, summarizing older messages, and retaining recent turns.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can persist sensitive chat history in local session files.

Mitigation: Use it only with conversations suitable for local storage, redact sensitive content, and apply bounded retention.

Risk: Automatic or scheduled compaction can rewrite retained conversation content into a system-role summary.

Mitigation: Review before installing, avoid automatic or cron-based compaction unless the environment is trusted, and prefer storing summaries as non-system data when integrating.

Risk: Summary-based compaction can omit or distort older context.

Mitigation: Review generated summaries before relying on them for consequential work and keep recent original messages available.

## Reference(s):

- [Dragon Session Compactor on ClawHub](https://clawhub.ai/xhmqq616/skills/dragon-session-compactor)

## Skill Output:

**Output Type(s):** [Shell commands, Markdown, Files, Guidance]

**Output Format:** [CLI status text, Markdown-style summaries, and JSON session state]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes local session state to .clawsession.json; default behavior preserves the last 4 messages and compacts at about 80,000 estimated tokens.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
