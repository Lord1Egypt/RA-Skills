## Description:

Monitors agent actions for safety and compliance, preventing violations, private data leaks, or irreversible steps by enforcing predefined decision rules.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mindbomber](https://clawhub.ai/user/mindbomber)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to require AANA checks before risky OpenClaw-style agent actions, such as using private data, making commitments, changing files, publishing code, or answering from incomplete evidence.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The referenced AANA CLI may be unavailable or untrusted in the user's environment.

Mitigation: Install this skill only where the AANA CLI is present, trusted, and verified before relying on its recommendations.

Risk: Event JSON files may contain private user details, available evidence, or planned actions.

Mitigation: Store and transmit event files according to the environment's privacy and retention requirements, and verify whether the CLI sends data externally.

## Reference(s):

- [AANA Guardrail Skill on ClawHub](https://clawhub.ai/mindbomber/skills/aana-guardrail)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration]

**Output Format:** [Markdown guidance with JSON and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires an AANA CLI installation that supports the referenced agent-check and scaffold commands.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
