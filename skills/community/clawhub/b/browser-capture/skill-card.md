## Description:

Guides an agent in using OpenClaw Browser to capture webpage screenshots and extract real content images while filtering out icons, logos, buttons, and avatars.

This skill is ready for commercial/non-commercial use.

## Publisher:

[n0nsense11](https://clawhub.ai/user/n0nsense11)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to operate OpenClaw Browser for webpage screenshots, image inspection, detail-page navigation, and downloading or saving higher-quality content images.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may download remote image URLs directly to local files.

Mitigation: Use trusted URLs and choose explicit, safe output paths before running download or copy commands.

Risk: The skill includes proxy advice around Cloudflare or other site protections.

Mitigation: Do not use the workflow to bypass bot checks, paywalls, login gates, or other access controls.

## Reference(s):

- [Browser Capture on ClawHub](https://clawhub.ai/n0nsense11/skills/browser-capture)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance, files]

**Output Format:** [Markdown guidance with OpenClaw browser shell commands and optional screenshot or image files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires OpenClaw >=0.15 and an available OpenClaw Browser session.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
