## Description:

Compress or convert generated images for delivery, preview, and social upload.

This skill is ready for commercial/non-commercial use.

## Publisher:

[632657122](https://clawhub.ai/user/632657122)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and content teams use this skill to compress, convert, and prepare generated image files for preview, delivery, and social upload.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The package bundles image-generation runtime code beyond the advertised compression workflow, including code paths that can handle API keys and send prompts or images to WeryAI.

Mitigation: Review the package before installing and remove or clearly separate the bundled image-generation runtime from the compression-only skill.

Risk: Secret-handling behavior in bundled code may persist API keys from this package context.

Mitigation: Do not configure or persist API keys through this package unless the image-generation runtime is intentionally retained and reviewed.

Risk: Runtime dependencies and local compressor tools may vary across environments.

Mitigation: Confirm the readiness check passes, install at least one supported compressor, and pin or vendor runtime dependencies before deployment.

Risk: Same-extension compression can overwrite the original file unless the user chooses the keep behavior or a separate output path.

Mitigation: Write outputs to a separate directory or use the keep behavior when compressing to the same extension.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/632657122/skills/compress-image)
- [Tool Selection Notes](references/tool-selection.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, code, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and optional JSON summaries from the compression CLI]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces compressed image files while preserving originals unless same-extension overwrite behavior is requested.]

## Skill Version(s):

9.0.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
