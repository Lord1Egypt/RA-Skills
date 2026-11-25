## Description:

Operate desktop applications on macOS, Windows, and Linux through native accessibility trees using the agent-desktop CLI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lahfir](https://clawhub.ai/user/lahfir)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and AI agents use this skill to inspect and operate desktop applications through accessibility trees, including navigation, form entry, screenshots, window management, and checking UI changes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Desktop-focus behavior and physical input may interrupt the active desktop or affect the wrong app.

Mitigation: Review the focus and headed-input behavior before use, target the intended desktop session, and use headed actions only when explicitly permitted.

Risk: A Chromium debugging endpoint may expose authenticated app access to local processes; the security scan also reports partial coverage of referenced material.

Mitigation: Review the CDP setup before enabling it, use it only with trusted local tooling, and inspect unresolved referenced material that is relevant to the deployment.

## Reference(s):

- [Agent Desktop on ClawHub](https://clawhub.ai/lahfir/skills/agent-desktop)
- [lahfir publisher profile](https://clawhub.ai/user/lahfir)
- [Interaction Commands](artifact/references/commands-interaction.md)
- [Observation Commands](artifact/references/commands-observation.md)
- [System Commands](artifact/references/commands-system.md)
- [Common Workflows](artifact/references/workflows.md)

## Skill Output:

**Output Type(s):** [Shell commands, JSON, Guidance]

**Output Format:** [Shell commands and JSON-based desktop interaction guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands can change desktop UI state; physical headed input requires explicit permission.]

## Skill Version(s):

0.1.34 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
