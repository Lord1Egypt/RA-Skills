## Description:

Generate and edit images with a bundled Gemini native image-generation CLI. Use when the user asks Codex to create images with Gemini, use Gemini image generation through a local bash CLI, run or debug Gemini image curl requests, choose Gemini image models/sizes/aspect ratios, inspect raw image-generation responses, or troubleshoot slow, timed-out, or failed Gemini image requests.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pluiez](https://clawhub.ai/user/pluiez)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to generate or edit images through Gemini-compatible endpoints with a local shell CLI. It is useful for choosing models, sizes, aspect ratios, provider modes, and troubleshooting image-generation requests.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends prompts and selected image files to a Gemini-compatible endpoint.

Mitigation: Install only when that data flow is acceptable, and prefer a local proxy when the runtime should not receive the real Google Gemini API key.

Risk: Undocumented --system and --system-file options can change request shaping.

Mitigation: Review those options before installation or modification, especially when using prompts or system text from files.

Risk: Retries or repeated generation requests can consume extra API quota or cost.

Mitigation: Confirm user intent before enabling retries, broad retries, or batch-style generation.

## Reference(s):

- [Gemini Image CLI Behavior](references/behavior.md)
- [gemini-balance local proxy](https://github.com/snailyp/gemini-balance)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance, files]

**Output Format:** [Markdown guidance with bash commands, stdout key-value result lines, and generated image/raw JSON files from the CLI.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Successful runs print image, raw_json, optional text, and duration_seconds paths or values.]

## Skill Version(s):

0.1.0 (source: release evidence and script VERSION)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
