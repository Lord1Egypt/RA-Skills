## Description:

Generate a project-local verify-<app> skill on top of e2e, so any coding agent can launch the app, check it is worth driving, exercise a feature the way a user does, keep evidence, and bug bash it. Writes the skill, a feature map with one explore charter per feature, and proves it once. Use for /create-verification-skill, "make a verification skill for this repo", or when a project has no scripted way to prove UI behavior.

This skill is ready for commercial/non-commercial use.

## Publisher:

[e2e](https://clawhub.ai/user/e2e)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and coding agents use this skill to inspect a project's user-facing app, create a project-local verification skill and feature map, and exercise the app through e2e to capture proof of behavior.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unpinned npx installer commands may fetch changed or compromised content.

Mitigation: Review the package and version that npx will resolve before running installer commands; pin versions where practical.

Risk: The scan was partial because some referenced paths were unresolved, so the security evidence is incomplete.

Mitigation: Review unresolved paths and complete a full scan before deployment.

Risk: Setup may change persistent agent or MCP configuration.

Mitigation: Review proposed configuration changes before allowing setup to apply them.

## Reference(s):

- [e2e project homepage](https://e2e.com)
- [create-verification-skill on ClawHub](https://clawhub.ai/e2e/skills/create-verification-skill)

## Skill Output:

**Output Type(s):** [Files, Markdown, Code, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Project-local Markdown skill and feature map, with e2e configuration and tests]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Tailored to the app surface, routes, run setup, and observable behavior found in the target project.]

## Skill Version(s):

1.0.3 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
