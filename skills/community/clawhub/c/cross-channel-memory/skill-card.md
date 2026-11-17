## Description:

Cross Channel Memory helps OpenClaw agents recognize the same user across QQ, Feishu, and related channels so they can locate and reuse the correct per-agent memory.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wljmmx](https://clawhub.ai/user/wljmmx)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators of OpenClaw agents use this skill to bind channel-specific user IDs to a unified user record and route memory lookup or write operations to the appropriate agent workspace.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Linked identities and conversation memory may be persisted with insufficient isolation.

Mitigation: Deploy only in controlled environments, require explicit opt-in from linked users, and enforce per-user memory isolation before production use.

Risk: Channel and user identifiers can route memory access incorrectly if they are not validated.

Mitigation: Validate identifiers before linking or lookup, use configurable OpenClaw paths, and treat stored user messages as untrusted data.

Risk: Conversation memory can remain available longer than users expect.

Mitigation: Define retention and deletion controls for stored user messages before enabling the skill for normal users.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wljmmx/skills/cross-channel-memory)
- [Artifact README](artifact/README.md)
- [Artifact skill definition](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands, JSON examples, and Python utility scripts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces mapping, lookup, memory synchronization, and session-hook guidance for OpenClaw agent workflows.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
