## Description:

Distill any commercial entity into a personalized brand agent with authentic voice, declared service capabilities, and a standard service contract.

This skill is ready for commercial/non-commercial use.

## Publisher:

[neiljo-gy](https://clawhub.ai/user/neiljo-gy)

### License/Terms of Use:

MIT-0

## Use Case:

Businesses, brands, studios, and institutions use this skill to create a customer-facing brand agent from existing brand material or direct brand declarations. The generated agent can expose declared information services, action services, third-party routing, behavior guidance, A2A discovery metadata, and a service contract.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill runs mutable npm tooling through npx/openpersona during generation.

Mitigation: Pin and verify the openpersona package version before generation, and run generation in a restricted workspace.

Risk: Generated brand agents may include broad command, file, and web permissions.

Mitigation: Remove broad default runtime tools unless a declared service capability truly requires them.

Risk: Generated agents can include persistence and ACN registration paths.

Mitigation: Require explicit user approval before enabling persistence or registering the agent on ACN or another external network.

## Reference(s):

- [ClawHub Release Page](https://clawhub.ai/neiljo-gy/skills/brand-persona-skill)
- [Service Contract Template](references/SERVICE-CONTRACT.template.md)
- [Behavior Guide Template](assets/behavior-guide.template.md)
- [Brand Persona Template](assets/brand.persona.template.json)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown, JSON, generated files, and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generates a self-contained brand persona skill directory with behavior guidance, service contract material, trigger mapping, and A2A discovery metadata when dependencies are available.]

## Skill Version(s):

0.1.0 (source: server release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
