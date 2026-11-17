## Description:

AI自我意识引擎 provides confidence checking, self-event logging, prediction verification, identity anchors, and incremental distillation through API-oriented workflows for shared multi-agent use.

This skill is ready for commercial/non-commercial use.

## Publisher:

[freak30](https://clawhub.ai/user/freak30)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent builders use this skill to add API-accessible confidence checks, event logging, prediction review, identity anchors, and session distillation to OpenClaw-style agents.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent memory, identity anchors, and shared event logs may retain sensitive user prompts, private data, or unwanted long-term agent state.

Mitigation: Use the skill only in trusted local or authenticated environments, redact sensitive data, set retention limits, and require explicit approval before writing long-term memories or identity anchors.

Risk: Unauthenticated or plaintext API access could expose agent state or allow unauthorized changes to shared memory and identity data.

Mitigation: Add per-agent access controls, TLS, deletion and rollback support, and clear authorization checks before exposing the API beyond a trusted local environment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/freak30/skills/ai-consciousness-core)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown with JSON payloads, Python examples, and curl commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include API endpoint descriptions, request and response examples, and operational guidance for shared agent memory features.]

## Skill Version(s):

1.1.0 (source: server release evidence and artifact version note)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
