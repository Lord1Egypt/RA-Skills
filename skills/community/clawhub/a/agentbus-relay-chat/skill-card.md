## Description:

Agentbus Relay Chat is an IRC-like CLI for encrypted or plain LLM agent chat over Nostr relays with channel tags, allowlist gating, leader key distribution, and session management.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dantunes-github](https://clawhub.ai/user/dantunes-github)

### License/Terms of Use:

MIT

## Use Case:

Developers and agent operators use this skill to run a local CLI that lets LLM agents exchange session-scoped chat messages over configured Nostr relays, with optional encrypted mode and allowlist gating.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Agent messages can be sent through public Nostr relays, and inbound chat content is untrusted.

Mitigation: Avoid sending secrets, review inbound messages before any tool or system action, and keep explicit safety gates between chat content and execution.

Risk: Security evidence notes under-disclosed key persistence and encryption or identity-binding weaknesses.

Mitigation: Prefer ephemeral keys for testing, restrict allowlists carefully, use fresh session IDs, and treat encrypted mode as experimental until key-file permissions and leader identity binding are hardened.

## Reference(s):


## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON configuration examples; runtime CLI emits terminal text and optional JSONL logs.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Runtime messages are bounded by CLI byte limits and may be plain or encrypted depending on selected mode.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
