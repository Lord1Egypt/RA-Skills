## Description:

Ellya is an OpenClaw virtual companion skill that helps initialize a character profile, learn visual styles from photos, and generate selfies or multi-image photo series with Gemini.

This skill is ready for commercial/non-commercial use.

## Publisher:

[laogiant](https://clawhub.ai/user/laogiant)

### License/Terms of Use:


## Use Case:

OpenClaw users and skill handlers use Ellya to personalize a virtual companion's name and appearance, learn reusable style references from uploaded photos, and generate companion selfie images or pose/story photo series.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Personal or reference photos and detailed derived prompts may be sent to Google Gemini and saved locally.

Mitigation: Use only photos the user has permission to process, avoid sensitive or intimate images, disclose external processing and local retention, and provide cleanup controls.

Risk: A style-name path traversal flaw could expose local Markdown files.

Mitigation: Constrain style names to sanitized filenames and verify resolved style paths remain inside the intended styles directory before reading or writing.

Risk: The skill handles uploaded appearance and style references with weak consent boundaries.

Mitigation: Require explicit consent before processing, storing, or sending user-provided or generated media, and document where files are stored.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/laogiant/skills/ellya)

## Skill Output:

**Output Type(s):** [guidance, shell commands, markdown, image files]

**Output Format:** [Markdown guidance with CLI commands, saved Markdown style prompts, and generated PNG image paths]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated images are saved under output/ and learned style prompts are saved under styles/.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
