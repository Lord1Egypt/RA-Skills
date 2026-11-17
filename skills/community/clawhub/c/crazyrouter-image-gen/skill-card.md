## Description:

Crazyrouter Image Gen generates images through the Crazyrouter API with selectable model, size, quality, and image count settings.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xujfcn](https://clawhub.ai/user/xujfcn)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to generate image files from text prompts via Crazyrouter when a user requests image creation, model selection, or image variations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Image prompts and generation settings are sent to Crazyrouter and may be handled by underlying model providers.

Mitigation: Install only if this data flow is acceptable, avoid sensitive prompts, and use a limited-scope CRAZYROUTER_API_KEY.

Risk: CRAZYROUTER_BASE_URL can redirect API calls to an environment-selected endpoint.

Mitigation: Leave CRAZYROUTER_BASE_URL unset unless the endpoint is fully trusted.

Risk: Generated images are written to the requested output path without overwrite protection.

Mitigation: Choose fresh filenames or an isolated output directory before running generation.

Risk: Downloaded image URLs are fetched without stronger URL validation or download limits.

Mitigation: Run in a controlled workspace and avoid untrusted endpoints until stronger validation and limits are added.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/xujfcn/skills/crazyrouter-image-gen)
- [Crazyrouter](https://crazyrouter.com)

## Skill Output:

**Output Type(s):** [Files, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown guidance with shell commands; generated image files are saved to user-selected paths.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires CRAZYROUTER_API_KEY and supports --model, --size, --n, and --quality options.]

## Skill Version(s):

1.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
