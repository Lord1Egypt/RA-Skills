## Description:

Guides users through obtaining, building, installing, and debugging the Andee Android agent, including a prebuilt-package route.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kuafuai](https://clawhub.ai/user/kuafuai)

### License/Terms of Use:

MIT-0

## Use Case:

Android users and developers use this skill to choose a prebuilt Andee package or follow a step-by-step source build, phone setup, and debugging workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The Android Accessibility service can read and act on the phone screen.

Mitigation: Enable it only on a device where you understand and accept that access.

Risk: An unauthenticated device-control WebSocket can be reachable over a network during debugging.

Mitigation: Do not expose it on public, shared, or untrusted networks; prefer adb-forwarded local debugging on an isolated device.

Risk: An optional WRITE_SECURE_SETTINGS grant provides elevated device access.

Mitigation: Avoid granting it unless the specific workaround is needed.

## Reference(s):

- [Andee skill release](https://clawhub.ai/kuafuai/skills/andee-skill)
- [Andee project repository (referenced by the skill)](https://github.com/kuafuai/andee)
- [CodeFlying Andee package route](https://www.codeflying.app/andee)
- [Get the code](references/get-the-code.md)
- [Build and install](references/build-and-install.md)
- [Debug loop](references/debug-loop.md)
- [CodeFlying route](references/codeflying-route.md)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration instructions]

**Output Format:** [Markdown with inline shell commands and step-by-step instructions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Route-specific steps with checks before proceeding.]

## Skill Version(s):

1.0.1 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
