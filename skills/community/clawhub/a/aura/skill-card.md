## Description:

Configure AI personality using the AURA protocol (HEXACO-based).

This skill is ready for commercial/non-commercial use.

## Publisher:

[phiro56](https://clawhub.ai/user/phiro56)

### License/Terms of Use:


## Use Case:

External users and developers use AURA to configure an agent's response personality, communication style, autonomy, and anti-sycophancy boundaries through a workspace AURA.yaml profile.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A workspace-level AURA.yaml profile can change the agent's response style and autonomy.

Mitigation: Review AURA.yaml before relying on the profile, especially in shared workspaces.

Risk: An optional AGENTS.md startup rule can make the personality profile persist across sessions.

Mitigation: Add startup rules only in trusted repositories and remove the rule manually if the profile should no longer load.

Risk: /aura reset removes AURA.yaml but may not remove any startup rule the user added separately.

Mitigation: After reset, check AGENTS.md or equivalent startup instructions for remaining AURA loading rules.

## Reference(s):

- [AURA protocol specification](https://github.com/phiro56/AURA)

## Skill Output:

**Output Type(s):** [Text, Markdown, Configuration, Guidance]

**Output Format:** [Markdown responses with YAML configuration examples and a workspace AURA.yaml profile]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create, display, or remove a local AURA.yaml personality profile; optional AGENTS.md startup guidance is user-applied.]

## Skill Version(s):

0.1.0-beta.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
