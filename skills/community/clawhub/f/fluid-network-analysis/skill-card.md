## Description:

Design, validate, solve, and analyze schema 1.0 steady-state incompressible fluid networks from TOML or natural-language requirements.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhang1jing2](https://clawhub.ai/user/zhang1jing2)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to create, validate, solve, and report on steady-state incompressible fluid network models from TOML or natural-language requirements. It supports pressure, flow, velocity, explicit operating-scenario, and deterministic function-availability analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated or copied TOML may encode incorrect units, missing assumptions, or unsupported operating conditions.

Mitigation: Review TOML before analysis, convert inputs to SI units, and document assumptions before relying on results.

Risk: Solver output may be mistaken for validated engineering truth.

Mitigation: Treat pressure, flow, velocity, and function-availability results as engineering aids and verify them with domain review.

Risk: The skill does not support transient, compressible, thermal, or probabilistic reliability simulation.

Mitigation: Use the skill only for schema 1.0 steady-state incompressible networks and state unsupported analyses explicitly.

## Reference(s):

- [TOML Schema 1.0 Reference](references/schema.md)
- [Simple Network Example](assets/simple_network.toml)
- [Redundant Supply Example](assets/redundant_supply.toml)
- [ClawHub Skill Page](https://clawhub.ai/zhang1jing2/skills/fluid-network-analysis)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown and JSON reports with inline shell commands and TOML configuration]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Python 3.9 or newer; no third-party Python packages are required.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
