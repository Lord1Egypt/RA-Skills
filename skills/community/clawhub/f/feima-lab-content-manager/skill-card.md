## Description:

Feima Lab Content Manager helps agents turn source text or Markdown into feima-lab styled MDX posts with local previews, image localization, metadata management, and optional authenticated backend save, publish, unpublish, listing, tagging, and upload workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fangshan101-coder](https://clawhub.ai/user/fangshan101-coder)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and content authors use this skill to create, preview, and manage feima-lab blog or news content from natural language, Markdown, and image inputs. Teams with the required internal API key can also use it to save, publish, unpublish, list, tag, and upload content through the feima-lab backend.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Remote save, publish, unpublish, tag, and upload actions can change backend content.

Mitigation: Use the skill only with a trusted publisher and require human review before running any remote write or publish command.

Risk: The skill requires an internal FX_AI_API_KEY for backend operations.

Mitigation: Keep the key in the shell environment only and do not store it in MEMORY.md, generated files, or other persistent project state.

Risk: Image localization and upload workflows may fetch URLs or read local image paths.

Mitigation: Avoid untrusted MDX and image URLs unless path containment and outbound-fetch restrictions are in place.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/fangshan101-coder/skills/feima-lab-content-manager)
- [README](README.md)
- [API publish workflow](references/api-publish-workflow.md)
- [API error handling](references/api-error-handling.md)
- [Component selection](references/component-selection.md)
- [Meta schema](references/meta-schema.md)
- [feima style snapshot](references/feima-style-snapshot.json)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, API calls, files, guidance]

**Output Format:** [Markdown guidance with shell commands plus generated MDX, HTML preview, image, and JSON metadata files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Remote publishing actions require Node 18+ and an internal FX_AI_API_KEY environment variable.]

## Skill Version(s):

1.5.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
