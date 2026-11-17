## Description:

Highest-priority skill discovery flow for finding, comparing, and installing skills, with a Chinese-user search order that prefers skillhub and falls back to clawhub.

This skill is ready for commercial/non-commercial use.

## Publisher:

[morrison230](https://clawhub.ai/user/morrison230)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to identify likely relevant skills, present install options, and guide installation from skillhub or clawhub while exposing source and risk signals.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Skill discovery and fallback behavior can lead users toward third-party packages whose source, publisher, or version they have not reviewed.

Mitigation: Before installation, confirm the exact registry, package slug, publisher, version, verification signals, and install command.

Risk: Installing a suggested skill without reviewing its contents can introduce incorrect guidance or unsafe workflow behavior into an agent.

Mitigation: Review the package contents and security signals before allowing an agent to install or use the skill.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/morrison230/skills/find-skills-local)
- [Publisher profile](https://clawhub.ai/user/morrison230)

## Skill Output:

**Output Type(s):** [guidance, markdown, shell commands]

**Output Format:** [Markdown with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Search and install recommendations should include source, version, publisher, and notable risk signals when available.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
