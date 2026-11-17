## Description:

Analyzes underwater reef images with YOLOv11 and MobileSAM to segment coral colonies and calculate coral coverage metrics.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mingzhuangwang](https://clawhub.ai/user/mingzhuangwang)

### License/Terms of Use:

MIT-0

## Use Case:

Marine ecologists, environmental agencies, and developers use this skill to route reef images through the OpenClaw API Gateway for coral segmentation, coverage-ratio calculation, and colony counts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Selected reef images and the OpenClaw token are sent to the OpenClaw API Gateway.

Mitigation: Install and use the skill only when this data transfer is acceptable, and avoid sending sensitive images or tokens outside approved workflows.

Risk: The example script writes visual output to coral_inference_result.jpg and may overwrite an existing file with that name.

Mitigation: Run the example from a directory where overwriting that filename is acceptable, or change the output filename before execution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mingzhuangwang/skills/coral-precise-coverage-ai)
- [OpenClaw coral prediction endpoint](https://api.openclaw.io/v1/skills/coral-precise-coverage-ai/predict)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with bash and Python examples; API responses are JSON with optional base64-encoded image output.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a reef image file and an OpenClaw API token.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
