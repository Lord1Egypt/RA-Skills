## Description:

Counts black Go/Weiqi stones from source board photos, estimates black Chinese-area scoring, and renders a clean static 19x19 result board image.

This skill is ready for commercial/non-commercial use.

## Publisher:

[imcaptor](https://clawhub.ai/user/imcaptor)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to analyze original 19x19 Go board photos, report visible black stones or black Chinese-area score, and optionally produce verification and result-board images.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Dependency ranges can change local image-processing behavior over time.

Mitigation: Install in a dedicated virtual environment or container and prefer pinned, hash-locked dependency versions.

Risk: Blurry, cropped, obstructed, scoring-overlay, or unsettled-dead-stone board images can produce incorrect counts or area estimates.

Mitigation: Review the generated overlay/result board, pass manual corners when board detection is wrong, and state manual confirmation is needed when warnings or life-and-death uncertainty remain.

## Reference(s):

- [ClawHub Skill Listing](https://clawhub.ai/imcaptor/skills/count-go-black-stones)
- [English README](https://github.com/imcaptor/count-go-black-stones/blob/main/README.en.md)

## Skill Output:

**Output Type(s):** [text, json, image files, shell commands, guidance]

**Output Format:** [Human-readable text or JSON, with optional generated overlay and result-board image files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a Go board image input; output quality depends on board visibility, grid detection, and life-and-death status.]

## Skill Version(s):

0.1.5 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
