## Description:

Pixelate chat and messaging app screenshots to hide chat titles, profile pictures, and display names.

This skill is ready for commercial/non-commercial use.

## Publisher:

[frankz2020](https://clawhub.ai/user/frankz2020)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use ChatMask to redact identity elements in chat screenshots before sharing them. The skill guides an agent to locate requested chat names, avatars, or display names and invoke a local image-pixelation workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup installs and runs code and dependencies fetched from outside the submitted skill package.

Mitigation: Review the upstream source, verify the pinned commit before installation, and run setup in a restricted environment.

Risk: Setup may attempt a host package-manager install if Python virtualenv support is missing.

Mitigation: Avoid running setup with root or broad package-manager privileges; preinstall required system packages through an approved environment image when possible.

## Reference(s):

- [ChatMask GitHub repository](https://github.com/frankz2020/chatmask)
- [ChatMask ClawHub skill page](https://clawhub.ai/frankz2020/skills/chatmask)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, code, files]

**Output Format:** [Markdown with inline bash commands and JSON bounding-box prompts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces locally processed pixelated image files after per-image analysis.]

## Skill Version(s):

1.1.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
