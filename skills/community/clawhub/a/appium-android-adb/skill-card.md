## Description:

Enables an agent to read and control a USB-connected Android phone through screen inspection, taps, swipes, and text entry.

This skill is ready for commercial/non-commercial use.

## Publisher:

[openlittlebear](https://clawhub.ai/user/openlittlebear)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and other users can direct an agent to inspect and interact with their USB-connected Android phone for app workflows, including navigation and form entry.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Direct phone controls can submit orders or interact with payment-adjacent screens without enforcing confirmation.

Mitigation: Require explicit human confirmation before booking, checkout, order submission, payment-adjacent taps, or entering sensitive information.

Risk: A running Appium server provides control of the connected phone.

Mitigation: Bind Appium to 127.0.0.1, prefer one-shot commands, and stop the daemon after use.

Risk: Screen captures and recognized text can reveal personal information.

Mitigation: Limit access to captured data and clear stored screenshots after use.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/openlittlebear/skills/appium-android-adb)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Guidance]

**Output Format:** [Text and JSON command responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Screen observations and action results may contain personal information.]

## Skill Version(s):

1.5.0 (source: server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
