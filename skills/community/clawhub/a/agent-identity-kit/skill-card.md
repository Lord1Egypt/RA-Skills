## Description:

Create, validate, and manage agent identity cards (agent.json) following the Agent Card v1 schema with interactive setup and validation tools.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ryancampbell](https://clawhub.ai/user/ryancampbell)

### License/Terms of Use:


## Use Case:

Developers and agent publishers use this skill to create and validate portable agent identity cards for publication at well-known URLs and registry indexing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Validation may fetch unpinned dependencies when local tooling is missing.

Mitigation: Pin and preinstall validation dependencies in CI or local environments before running the skill.

Risk: Validation of untrusted paths can execute attacker-controlled code through the fallback validator.

Mitigation: Do not run validate.sh on paths supplied by others until path handling is fixed; use a preinstalled, pinned validator instead.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ryancampbell/skills/agent-identity-kit)
- [Agent Card specification](https://foragents.dev/spec/agent-card)
- [Agent Card v1 JSON Schema](https://foragents.dev/schemas/agent-card/v1.json)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration]

**Output Format:** [Markdown guidance with shell commands and generated JSON agent-card files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated agent cards are intended to follow the Agent Card v1 JSON Schema.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
