## Description:

Direct Emporia Vue energy queries via Emporia cloud (PyEmVue) or local ESPHome API, including guidance on choosing/configuring cloud vs local modes and running list/summary/circuit commands.

This skill is ready for commercial/non-commercial use.

## Publisher:

[urosorozel](https://clawhub.ai/user/urosorozel)

### License/Terms of Use:


## Use Case:

Developers and technically proficient energy-monitoring users use this skill to configure cloud or local access to Emporia Vue data and run summary, list, or circuit-level energy queries from an agent.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The cloud login path can connect to an arbitrary simulator host when EMPORIA_EMAIL begins with vue_simulator@.

Mitigation: Use only trusted configuration values and avoid vue_simulator@ email values unless simulator behavior is intentional and reviewed.

Risk: The skill handles sensitive Emporia account credentials and ESPHome API secrets.

Mitigation: Run it in an isolated virtual environment with only the Emporia or ESPHome secrets required for the selected mode.

Risk: The ESPHome dependency is not pinned to an exact version.

Mitigation: Pin and review the aioesphomeapi dependency before deployment.

## Reference(s):

- [Emporia Energy Skill References](references/README.md)
- [ClawHub Skill Page](https://clawhub.ai/urosorozel/skills/emporia-energy)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, JSON]

**Output Format:** [Markdown guidance with shell commands and JSON script output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Scripts emit timestamped summary, list, and circuit-query payloads with mode, unit, total, top circuits, and channels used when available.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
