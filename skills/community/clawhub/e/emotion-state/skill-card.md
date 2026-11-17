## Description:

Adds natural-language emotion tracking to an OpenClaw hook and injects a compact emotion_state block into the system prompt.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tashfeenahmed](https://clawhub.ai/user/tashfeenahmed)

### License/Terms of Use:


## Use Case:

Developers and agent operators use this skill to add session-aware emotion summaries to OpenClaw agents so prompts can include recent user, agent, and trend context.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Emotion profiling and persistent state may expose sensitive user or agent context.

Mitigation: Use only where users and agents have consented, avoid sensitive conversations unless retention controls are added, and provide deletion controls for stored emotion state.

Risk: Prompt injection of inferred emotion state can influence downstream agent behavior.

Mitigation: Review the injected emotion_state block behavior before deployment and limit use to agents where this context is appropriate.

Risk: Classifier configuration can send conversation text to an external or arbitrary endpoint.

Mitigation: Prefer a trusted local or tightly allowlisted classifier endpoint and avoid arbitrary OPENAI_BASE_URL values.

Risk: Cross-agent state reads may expose emotion summaries across agent boundaries.

Mitigation: Restrict filesystem access between agents and disable or constrain cross-agent state sharing where isolation is required.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/tashfeenahmed/skills/emotion-state)
- [Publisher profile](https://clawhub.ai/user/tashfeenahmed)
- [OpenAI API base URL](https://api.openai.com/v1)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Files]

**Output Format:** [Markdown instructions with shell commands and JSON configuration; the runtime hook injects an XML-like emotion_state text block and writes JSON state.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Stores model-inferred emotion labels, reasons, confidence, timestamps, source hashes, and trend summaries in a per-agent state file.]

## Skill Version(s):

1.2.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
