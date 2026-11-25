## Description:

Read game controllers correctly in the browser with the Gamepad API and build controller testers that measure stick drift, circularity, built-in deadzones, analog triggers and vibration. Use when writing or debugging web code that calls navigator.getGamepads(), listens for gamepadconnected, or handles controller input in a game or tester page.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hlplanet](https://clawhub.ai/user/hlplanet)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill when writing or debugging browser games and controller tester pages. It guides them in detecting gamepads and interpreting controller mappings, axes, buttons, drift, circularity, deadzones, triggers, and vibration.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review was benign with medium confidence, but scan coverage was partial and two local path-like references could not be resolved.

Mitigation: Review the complete release contents and unresolved references before installing; the scan guidance also notes a low-likelihood context-stuffing concern.

Risk: Gamepad data can be unavailable outside secure contexts, in some cross-origin iframes, or while a page is hidden, which can disrupt controller tests.

Mitigation: Use HTTPS or localhost, allow gamepad access on cross-origin iframes where needed, and pause timed tests when the page becomes hidden.

## Reference(s):

- [HLPlanet gamepad tester](https://www.hlplanet.com/gamepad-tester/)
- [Testing controller polling rate outside the browser](https://www.hlplanet.com/how-to-test-polling-rate-of-controller/)
- [ClawHub release page](https://clawhub.ai/hlplanet/skills/browser-gamepad-input)

## Skill Output:

**Output Type(s):** [Code, Guidance]

**Output Format:** [Markdown with JavaScript examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [None]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
