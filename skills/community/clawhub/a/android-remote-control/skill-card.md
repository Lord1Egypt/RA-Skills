## Description:

Controls USB-debug-enabled Android devices through uiautomator2 and ADB to capture screenshots, tap coordinates, and launch apps.

This skill is ready for commercial/non-commercial use.

## Publisher:

[eyedark](https://clawhub.ai/user/eyedark)

### License/Terms of Use:


## Use Case:

Developers and device automation testers use this skill to inspect and drive connected Android devices during app workflows, including screenshots, taps, and app launches.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can manipulate a connected Android phone without clear safety gates.

Mitigation: Install only when remote device control is intended, review each requested tap or app launch, and avoid unattended use with sensitive apps.

Risk: The release evidence says the skill overstates some capabilities.

Mitigation: Treat documented install or uninstall behavior as unverified unless the artifact implementation supports it.

## Reference(s):


## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Code, Files]

**Output Format:** [Markdown with inline bash commands and generated device screenshot files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands target a locally connected Android device through ADB and uiautomator2.]

## Skill Version(s):

1.0.0 (source: release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
