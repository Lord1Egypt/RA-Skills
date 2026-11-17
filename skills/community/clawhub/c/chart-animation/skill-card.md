## Description:

Generate dark-themed animated trend charts and static overview images from time-series JSON data with customizable titles, frame rates, and chart dimensions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ravenquasar](https://clawhub.ai/user/ravenquasar)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and analysts use this skill to turn time-series JSON data into presentation-ready animated GIF or MP4 trend charts and static overview images.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Package metadata declares Python libraries as unpinned npm dependencies, which may create install-time supply-chain exposure if used directly.

Mitigation: Install the Python dependencies in a virtual environment with pinned versions and ignore or remove the npm dependency block unless those packages are intentionally used.

Risk: MP4 export depends on an external ffmpeg installation.

Mitigation: Install ffmpeg only from a trusted system package source, or use GIF and PNG outputs when ffmpeg is unavailable.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/ravenquasar/skills/chart-animation)
- [Chart Animation Examples](artifact/examples/README.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces guidance for generating animation.gif, animation.mp4 when ffmpeg is available, and overview.png from validated time-series JSON input.]

## Skill Version(s):

1.0.0 (source: artifact SKILL.md, package.json, and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
