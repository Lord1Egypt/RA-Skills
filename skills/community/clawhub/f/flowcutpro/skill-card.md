## Description:

FlowCutPro helps agents create cinematic multi-shot videos from text concepts by planning shots with an LLM, rendering clips with Google Veo 3, and stitching them with ffmpeg.

This skill is ready for commercial/non-commercial use.

## Publisher:

[windseeker1111](https://clawhub.ai/user/windseeker1111)

### License/Terms of Use:

MIT-0

## Use Case:

External creators, marketers, and developers use FlowCutPro to turn text briefs into multi-shot cinematic videos, reels, TikToks, and commercials. The skill is intended for agents that can produce shot plans, run rendering commands, and guide users through video-generation setup and output handling.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A hardcoded fallback Google API key could expose credentials or allow unintended use.

Mitigation: Remove the fallback key, rotate any exposed key, and require credentials to come only from a user-managed secret such as VEO_API_KEY.

Risk: Prompt and credential handling may disclose user content or API keys to external services.

Mitigation: Clearly disclose external LLM and Google Veo 3 calls, and prefer platform-managed LLM and credential paths where available.

Risk: Generated video download URLs may be fetched without trusted-host validation.

Mitigation: Validate download URLs against trusted Google hosts before retrieving video artifacts.

## Reference(s):

- [FlowCutPro ClawHub skill page](https://clawhub.ai/windseeker1111/skills/flowcutpro)
- [Google AI Studio API keys](https://aistudio.google.com/apikeys)
- [Google Generative Language API endpoint used by FlowCutPro](https://generativelanguage.googleapis.com/v1beta/models/veo-3.1-generate-preview:predictLongRunning)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files]

**Output Format:** [Markdown guidance with inline shell commands, generated JSON shot plans, and local MP4 output files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can produce dry-run shot plans or render video clips and a stitched final MP4 when configured with external API access.]

## Skill Version(s):

1.0.0 (source: frontmatter, package.json, release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
