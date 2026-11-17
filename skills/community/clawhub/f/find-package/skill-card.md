## Description:

Helps users locate packages on Chinese delivery station shelves by matching pickup codes from text or screenshots to shelf photos and returning annotated images.

This skill is ready for commercial/non-commercial use.

## Publisher:

[noroot777](https://clawhub.ai/user/noroot777)

### License/Terms of Use:

MIT-0

## Use Case:

External users in Chinese delivery station workflows use this skill through an OpenClaw Telegram Bot to submit pickup codes and shelf photos, then receive Chinese guidance and annotated photos marking likely matching packages.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Pickup-code screenshots and shelf photos may contain unrelated personal details or bystanders.

Mitigation: Ask users to crop or redact unrelated details where practical and avoid sharing unnecessary personal information.

Risk: Image recognition may be unreliable when shelf photos are blurry, poorly lit, or taken at a difficult angle.

Mitigation: Request clearer photos instead of guessing when package labels or pickup codes are unreadable.

Risk: The annotation helper depends on Pillow.

Mitigation: Install Pillow in a virtual environment with a pinned, reviewed version.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/noroot777/skills/find-package)
- [OpenClaw](https://openclaw.com)
- [Pillow documentation](https://pillow.readthedocs.io/)

## Skill Output:

**Output Type(s):** [text, shell commands, files, guidance]

**Output Format:** [Chinese chat messages, inline shell commands, and annotated image files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Annotated images use red bounding boxes and labels; image annotation requires Python 3 and Pillow.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
