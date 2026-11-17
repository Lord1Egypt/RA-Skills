## Description:

Distill anyone into a runnable OpenPersona skill pack, using chat logs, documents, and public content to extract persona dimensions and generate a portable OpenPersona pack.

This skill is ready for commercial/non-commercial use.

## Publisher:

[neiljo-gy](https://clawhub.ai/user/neiljo-gy)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to collect authorized source material, extract a structured persona profile, and generate a runnable OpenPersona skill pack for a real, fictional, historical, or synthetic subject.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles sensitive private communications and persona source files.

Mitigation: Use only data the operator is authorized to process, get consent for private third-party communications, and review collected material before creating a persona pack.

Risk: The skill can build personas that could be used for deception, harassment, or impersonation.

Mitigation: Apply the artifact's ethics rules: require personal-use confirmation for people the user knows, add disclaimers for public figures, and avoid deceptive deployment.

Risk: The workflow may run local shell commands and live npx OpenPersona commands.

Mitigation: Run in a restricted working directory and pin or preinstall OpenPersona instead of relying on live npx execution.

Risk: Rollback, update, or init operations with untrusted slug or version values can affect local skill files.

Mitigation: Do not use those commands with untrusted values until path validation is added; review target paths before execution.

## Reference(s):

- [Ethics & Copyright Reference](references/ethics.md)
- [Output Format Reference](references/output-format.md)
- [Training Data Export](references/training-export.md)
- [ClawHub skill page](https://clawhub.ai/neiljo-gy/skills/anyone-skill)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON configuration, generated skill-pack files, training-data files, and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include persona.json, persona.md, training data, metadata, and an OpenPersona-compatible skill pack.]

## Skill Version(s):

1.1.2 (source: server release metadata and skill frontmatter metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
