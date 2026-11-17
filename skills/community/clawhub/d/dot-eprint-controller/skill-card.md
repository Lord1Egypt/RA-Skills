## Description:

Controls Dot. e-paper devices by checking status, listing content, pushing text or images, and switching the displayed content.

This skill is ready for commercial/non-commercial use.

## Publisher:

[johnqxu](https://clawhub.ai/user/johnqxu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and device operators use this skill to manage a Dot. e-paper display through the Dot. API, including status checks, text or image updates, content listing, and manual content switching.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends the Dot API key and device content to dot.mindreset.tech.

Mitigation: Install and use it only when the user trusts that service with the API key and displayed content.

Risk: Text, image, and next-content commands can immediately alter the e-paper display.

Mitigation: Confirm the intended device ID and avoid sending sensitive text or images unless they are meant to appear on the device.

Risk: Image pushes depend on local image preprocessing with ImageMagick convert.

Mitigation: Verify ImageMagick is installed and inspect the selected image before uploading it to the device.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/johnqxu/skills/dot-eprint-controller)
- [Dot. API service](https://dot.mindreset.tech)

## Skill Output:

**Output Type(s):** [Text, Shell commands, API calls, Configuration guidance]

**Output Format:** [Markdown with inline bash commands and user-facing status summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires DOT_API_KEY and DOT_DEVICE_ID; image pushes require ImageMagick convert for local preprocessing.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
