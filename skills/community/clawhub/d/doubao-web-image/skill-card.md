## Description:

Uses Playwright browser automation to generate and download images from Doubao Web from a prompt, optional aspect ratio, quality setting, and output path.

This skill is for research and development only.

## Publisher:

[atmosphere16happy](https://clawhub.ai/user/atmosphere16happy)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users can use this skill to ask an agent to generate images through Doubao Web, including ratio, quality, and local save-path options. The artifact documentation frames the project for learning, Playwright automation testing, research, and technical exchange.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses a reusable Doubao web session and persistent browser profile data.

Mitigation: Install only where that account automation is acceptable, avoid global or root installation, and delete ~/.doubao-web-session when the session is no longer needed.

Risk: The security evidence flags stealth browser automation and high-resolution or watermark-free retrieval behavior for careful review.

Mitigation: Use a pinned reviewed release and confirm that the intended use complies with Doubao platform terms and generated-content policies before deployment.

Risk: Caller-controlled output paths and debug artifacts may expose private account or generated-content data.

Mitigation: Restrict output paths to a safe folder and treat debug screenshots and HTML as private data.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/atmosphere16happy/skills/doubao-web-image)
- [ClawHub publisher profile](https://clawhub.ai/user/atmosphere16happy)
- [Artifact README](artifact/README.md)
- [Artifact skill definition](artifact/SKILL.md)
- [Doubao Web chat](https://www.doubao.com/chat/)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, files, guidance]

**Output Format:** [Text or Markdown status with shell command usage and a local generated image file path]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May save an image to a caller-selected path and may create local debug screenshots or HTML during failures.]

## Skill Version(s):

1.0.0 (source: server release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
