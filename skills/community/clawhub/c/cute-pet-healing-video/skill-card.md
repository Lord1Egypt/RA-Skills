## Description:

Generate vertical healing-style cute pet shorts with WeryAI from text prompts or one pet image, using soft motion, warm light, slow pacing, and optional ambience for short-video feeds.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zoucdr](https://clawhub.ai/user/zoucdr)

### License/Terms of Use:

MIT-0

## Use Case:

External creators and developers use this skill to plan and run WeryAI text-to-video or image-to-video pet shorts with confirmed model parameters, prompt expansion, and returned video URLs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts, selected images, and WERYAI_API_KEY are sent to WeryAI during normal use.

Mitigation: Install only if the publisher is trusted, keep WERYAI_API_KEY out of the package and source control, and use an isolated or short-lived runtime for higher assurance.

Risk: The bundled CLI can upload any readable local file supplied through image fields.

Mitigation: Prefer public HTTPS image URLs. Use local paths or file:// URLs only after reviewing the script and confirming the exact file should be uploaded.

Risk: Successful wait runs consume paid WeryAI credits.

Mitigation: Confirm model, duration, resolution, audio, prompt, and image inputs before generation; use dry-run for request inspection when appropriate.

## Reference(s):

- [Cute Pet Healing Video on ClawHub](https://clawhub.ai/zoucdr/skills/cute-pet-healing-video)
- [WeryAI Video CLI and JSON](resources/WERYAI_VIDEO_API.md)
- [WeryAI video API host](https://api.weryai.com)
- [WeryAI models and upload API host](https://api-growth-agent.weryai.com)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands, JSON request payloads, and returned video URLs or error details.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js 18+, WERYAI_API_KEY, network access, and WeryAI credits for successful generation runs.]

## Skill Version(s):

1.0.5 (source: server release evidence; artifact frontmatter and _meta.json report 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
