## Description:

Openclaw Context Capsule compresses older OpenClaw agent session history into a bounded, lane-change-aware context capsule while keeping recent messages verbatim, redacting credential-shaped secrets, and quarantining injected instructions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[parad0x-labs](https://clawhub.ai/user/parad0x-labs)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to reduce prompt tokens in long OpenClaw sessions while keeping recent turns and important older decisions, tasks, errors, paths, links, and durable facts available to the model.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Older session history is summarized rather than preserved verbatim, so exact wording, nuance, or low-priority details can be lost.

Mitigation: Use the skill for long-running sessions where bounded context is acceptable; keep original logs or retrieval sources available when exact transcript fidelity is required.

Risk: Credential-shaped secrets are redacted on a best-effort basis, but semantic personal or confidential details may still appear in retained context.

Mitigation: Do not treat the skill as the only privacy control for highly sensitive chats; limit sensitive inputs and apply host-level data handling controls.

## Reference(s):

- [Openclaw Context Capsule ClawHub listing](https://clawhub.ai/parad0x-labs/skills/context-capsule)
- [README](README.md)
- [Changelog](CHANGELOG.md)

## Skill Output:

**Output Type(s):** [text, JSON, configuration]

**Output Format:** [Model-readable text capsule with JSON-compatible capsule metadata and OpenClaw configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Older history is lossy and bounded by maxCapsuleTokens and capsuleTokenRatio; recent messages are retained verbatim.]

## Skill Version(s):

1.6.1 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
