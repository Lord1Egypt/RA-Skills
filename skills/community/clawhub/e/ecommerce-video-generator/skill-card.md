## Description:

Generates e-commerce video request payloads by reading storyboard JSON, condensing script text, extracting duration and product imagery, and optionally submitting the payload to the configured AIGC service.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bstory28](https://clawhub.ai/user/bstory28)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and e-commerce content teams use this skill at the final stage of an international e-commerce video pipeline to turn upstream storyboard and product image files into a compressed script and video generation payload. The skill supports preview-only payload generation and optional submission to an approved AIGC service.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Storyboard text, product image data, and payload metadata may be saved locally and sent to an external AIGC service when submit mode is used.

Mitigation: Use preview mode first, review the generated payload, and submit only material approved for the configured AIGC service.

## Reference(s):

- [Server-resolved source repository](https://github.com/BStory28/ecommerce-video-generator)
- [ClawHub skill page](https://clawhub.ai/bstory28/skills/ecommerce-video-generator)
- [Upstream product info generator](https://github.com/BStory28/ecommerce-product-info-generator)
- [Upstream video script generator](https://github.com/BStory28/ecommerce-video-script-generator)

## Skill Output:

**Output Type(s):** [text, markdown, configuration]

**Output Format:** [Markdown status text plus JSON payload files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes compressed_script.txt and video_payload.json; submit mode can send the payload to the configured AIGC service.]

## Skill Version(s):

0.1.0 (source: server release metadata; artifact frontmatter declares 1.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
