## Description:

Read Figma files, extract design tokens, generate React Native Expo TypeScript or Web React with Tailwind code, create plugin-compatible write-back specs, and diff local design models against Figma.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kristinadarroch](https://clawhub.ai/user/kristinadarroch)

### License/Terms of Use:


## Use Case:

Developers and design engineers use this skill to turn Figma files into design models, tokens, and application code, then review diffs or plugin-compatible operation specs for design updates.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unsafe cache path handling could allow unintended local writes.

Mitigation: Review file keys and patch specs before use, run commands from a constrained project directory, and avoid broad filesystem permissions.

Risk: Weak write-back validation could produce malformed or unintended Figma plugin operations.

Mitigation: Keep write-back dry-run by default, inspect generated pluginSpec.json and warnings, and use --execute only with the companion plugin flow understood.

Risk: Web React with Tailwind support is described as secondary and incomplete by the security guidance.

Mitigation: Treat Web React with Tailwind output as a starting point that needs manual review before production use.

## Reference(s):

- [DesignSpec Schema](artifact/references/design-spec-schema.json)
- [Figma REST API Guide](artifact/references/api-guide.md)
- [Figma API Access Tokens](https://www.figma.com/developers/api#access-tokens)
- [Figma API Base URL](https://api.figma.com)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and generated JSON, TypeScript, React Native, React, Tailwind, and plugin operation files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Pull operations write designModel.json, tokens.json, codePlan.json, and component files; diff and preview operations write JSON summaries and patch specs.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
