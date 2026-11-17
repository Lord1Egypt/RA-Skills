## Description:

Chrome UI automation skill for saving named on-screen targets and reusing them with reliable click/type actions when browser selectors break or deterministic named-point flows are needed.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jayton123456789-hub](https://clawhub.ai/user/jayton123456789-hub)

### License/Terms of Use:


## Use Case:

Developers and automation users use ClickMap to mark named browser UI points, sync them through a local bridge, and have an agent list, click, type into, or click-type those saved targets for repetitive web tasks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The Chrome extension can be active on all sites and saved POIs may include page targets, selectors, viewport coordinates, and screen coordinates.

Mitigation: Use the skill only on pages where mapping UI targets is acceptable, avoid mapping sensitive pages when possible, and review stored POIs before automation runs.

Risk: The local bridge stores browser automation targets and the security summary reports unsafe default access controls.

Mitigation: Set CLICKMAP_TOKEN, keep the bridge bound to localhost, and do not expose the bridge port beyond the local machine.

Risk: Synced or imported POIs can change where future automation clicks or types.

Mitigation: Treat imported or synced POI data as operationally sensitive and verify target names and coordinates before executing click or type actions.

## Reference(s):


## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with PowerShell command examples and JSON POI data]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May rely on named POIs with screen coordinates and local bridge state.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
