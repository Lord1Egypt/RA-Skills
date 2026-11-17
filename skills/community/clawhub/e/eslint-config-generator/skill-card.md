## Description:

Generates ESLint configuration guidance and example configs for common JavaScript, React, Vue, TypeScript, Airbnb, Standard, and Prettier presets.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sunshine-del-ux](https://clawhub.ai/user/sunshine-del-ux)

### License/Terms of Use:

MIT

## Use Case:

Developers use this skill to create ESLint configuration guidance and baseline .eslintrc.json content for JavaScript and TypeScript projects that use common style presets.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The bundled script can silently overwrite an existing .eslintrc.json file.

Mitigation: Run it only in a disposable or backed-up project directory, or update the script to require explicit confirmation before overwriting an existing config.

Risk: The preset value is written into JSON without validation.

Mitigation: Use only trusted preset values and update the script to allowlist supported presets and escape JSON safely.

## Reference(s):

- [ESLint Config Generator ClawHub Page](https://clawhub.ai/sunshine-del-ux/skills/eslint-config-generator)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with bash and JSON snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce or overwrite .eslintrc.json when the bundled shell script is executed.]

## Skill Version(s):

1.0.0 (source: server release metadata, artifact/_meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
