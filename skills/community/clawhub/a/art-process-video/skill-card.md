## Description:

Generate vertical short videos of painting and retouching creative processes with WeryAI, showing layered progression from sketch to finished art.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zoucdr](https://clawhub.ai/user/zoucdr)

### License/Terms of Use:

MIT-0

## Use Case:

External creators, designers, and agents use this skill to turn text briefs or public HTTPS image inputs into WeryAI-generated vertical art-process videos. It is intended for painting timelapse, design creation reels, image-to-video color progression, and short-form creative storytelling.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires WERYAI_API_KEY and sends prompts, image URLs, and generation requests to WeryAI services.

Mitigation: Provide the API key only in trusted runtime environments, never commit it to the skill package, and review any WERYAI_BASE_URL or WERYAI_MODELS_BASE_URL override before running.

Risk: Successful wait runs consume paid WeryAI credits.

Mitigation: Use the pre-submit confirmation step to review the full prompt and parameters before starting generation.

Risk: Unsupported model, duration, aspect ratio, resolution, or local image inputs can cause failed generation requests.

Mitigation: Keep parameters within the documented WeryAI model constraints and use only public HTTPS image URLs.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/zoucdr/skills/art-process-video)
- [WeryAI API Service](https://api.weryai.com)
- [WeryAI Models Service](https://api-growth-agent.weryai.com)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON result summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns WeryAI task status, task IDs, generated video URLs, cover URLs, or structured error details when available.]

## Skill Version(s):

0.1.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
