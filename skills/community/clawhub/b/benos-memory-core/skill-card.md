## Description:

Core runtime/volatile memory module for the BenOS agent environment that stores and retrieves active session state, open loops, decisions, and scratch notes at runtime.

This skill is ready for commercial/non-commercial use.

## Publisher:

[benmjohnson69](https://clawhub.ai/user/benmjohnson69)

### License/Terms of Use:


## Use Case:

Developers and agent operators use this skill to hydrate BenOS agents with runtime memory, prior-session text, open loops, recent decisions, and notes stored in local BenOS state files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can expose prior-session text and runtime state from local BenOS memory files to agents that invoke it.

Mitigation: Install it only for trusted agent environments, treat the runtime files as sensitive, and add authorization or redaction controls when per-agent isolation is needed.

## Reference(s):

- [ClawHub skill release page](https://clawhub.ai/benmjohnson69/skills/benos-memory-core)

## Skill Output:

**Output Type(s):** [text, json]

**Output Format:** [JSON object containing status, messages, and hydrated runtime state]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reads fixed local BenOS runtime files under the user's home directory when hydration is requested.]

## Skill Version(s):

0.1.2 (source: skill.json and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
