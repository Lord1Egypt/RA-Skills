## Description:

Doubao API Toolkit helps agents use Volcengine ARK APIs for text-to-image, image-to-image, text-to-video, image and video analysis, and task status checks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[systiger](https://clawhub.ai/user/systiger)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and automation agents use this skill to call Doubao and Volcengine ARK multimodal APIs from Python or the CLI for media generation, visual analysis, and video task management.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The video-analysis command can upload any readable local file path selected by a prompt or automation workflow.

Mitigation: Use analyze-vid only with intentional, non-sensitive media from a dedicated folder, and add confirmation plus file type and size checks before automated use.

Risk: Prompts, image URLs, and selected local videos are sent to Volcengine ARK using the configured ARK_API_KEY.

Mitigation: Use a dedicated API key, keep it in the environment rather than source files, rotate it regularly, and avoid sending confidential media or prompts.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/systiger/skills/doubao-api-toolkit)
- [Volcengine ARK Documentation](https://www.volcengine.com/docs/82379)
- [Doubao Model Pricing](https://console.volcengine.com/ark)
- [OpenClaw Documentation](https://docs.openclaw.ai)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with CLI commands, Python usage examples, JSON response examples, and generated local media file paths.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3, the requests library, and ARK_API_KEY. Generated images and videos are saved under ~/.openclaw/workspace/output.]

## Skill Version(s):

1.0.0 (source: frontmatter, skill.json, release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
