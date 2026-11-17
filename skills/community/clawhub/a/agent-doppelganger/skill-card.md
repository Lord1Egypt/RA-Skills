## Description:

Constrained autonomous delegate for identity-proxied communication. Handles incoming messages (Email, Discord, Slack, WhatsApp) by analyzing intent and applying declarative authority policies before generating responses. Use when the user wants to delegate communication tasks while maintaining identity fidelity and enforcing strict non-overreach boundaries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sieershafilone](https://clawhub.ai/user/sieershafilone)

### License/Terms of Use:

Apache-2.0

## Use Case:

Developers and operators use this skill to delegate low-stakes communication handling while enforcing policy, confidence, and escalation boundaries before any response is sent or drafted.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can reply as the user while key safety checks are still placeholder-level.

Mitigation: Keep the skill in draft-only or block mode until policy checks, confidence scoring, and final verification fail closed under review.

Risk: Private communications and identity profile data may be stored locally through audit, memory, and profile files.

Mitigation: Minimize and redact stored data, enforce short retention, and require explicit approval before profile or memory writes.

Risk: Real channel-send authority could create identity, reputation, or commitment risk.

Mitigation: Do not grant direct send permissions or broad access to private channels until installation-specific policies and escalation behavior are tested.

Risk: Watermarking and disclosure behavior may be unclear to users or affected recipients.

Mitigation: Make automated-delegate disclosure and watermark controls transparent and user-controlled before deployment.

## Reference(s):

- [Agent Doppelgänger Specification](references/specification.md)

## Skill Output:

**Output Type(s):** [Text, Configuration, Guidance]

**Output Format:** [Plain text responses, decision labels, and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create local audit and profile files when run by an agent.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact manifest lists 0.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
