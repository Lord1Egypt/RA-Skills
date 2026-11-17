## Description:

Captures images from Dahua Cloud-connected IoT devices, saves the snapshot locally, and sends the image to Dahua Cloud image analysis for prompts about people, vehicles, objects, safety equipment, smoke, fire, falls, intrusion, and other monitored-scene conditions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[doynkdeveloper](https://clawhub.ai/user/doynkdeveloper)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, operators, and safety teams use this skill to capture authorized Dahua device camera snapshots and ask Dahua Cloud to analyze the image for operational, inspection, security, and safety-monitoring questions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles surveillance images and Dahua Cloud credentials.

Mitigation: Use it only for cameras and scenes you are authorized to capture and send to Dahua Cloud, use least-privilege credentials, avoid exposing DAHUA_CLOUD_SK in logs or screenshots, and rotate keys if exposure is suspected.

Risk: Captured images are saved locally and may contain sensitive visual information.

Mitigation: Run the skill from a restricted working directory or dedicated account, treat captured_images as sensitive, and add retention controls appropriate to the deployment.

Risk: The security verdict is suspicious due to under-scoped safety controls around credentials, image handling, logging, and downloaded URLs.

Mitigation: Review before installing, validate device IDs, restrict downloaded URLs where possible, reduce logging of sensitive request data, and pin dependencies.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/doynkdeveloper/skills/dahua-cloud-open-device-image-analysis)
- [Dahua Cloud Open Platform](https://open.cloud-dahua.com/)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands, Python examples, local image paths, and JSON-like analysis results.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Dahua Cloud Product ID, Access Key, and Secret Key environment variables; captures images into captured_images and returns the Dahua Cloud analysis result.]

## Skill Version(s):

1.0.5 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
