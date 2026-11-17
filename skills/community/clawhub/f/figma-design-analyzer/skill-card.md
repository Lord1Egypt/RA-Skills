## Description:

Analyzes Figma design files to extract design system data, export screenshots, and compare designs with implementation files.

This skill is ready for commercial/non-commercial use.

## Publisher:

[plume-lj](https://clawhub.ai/user/plume-lj)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and design engineers use this skill to inspect Figma files, extract colors, fonts, spacing, components, and screenshots, and check whether CSS or code implementations match the design source.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Figma access tokens can expose private design files if stored or shared improperly.

Mitigation: Use a token with the minimum needed access, keep .env files out of version control, and rotate the token if it is exposed.

Risk: Figma file metadata, comments, versions, design structure, and screenshots may be retrieved and stored locally.

Mitigation: Run the skill only on files the user is authorized to access and review generated files before sharing or committing them.

Risk: Dependencies are installed at runtime and may change without a lockfile.

Mitigation: Install from a verified package or repository and review dependencies or use a lockfile before deployment.

## Reference(s):

- [Figma API Reference](references/figma-api.md)
- [ClawHub skill page](https://clawhub.ai/plume-lj/skills/figma-design-analyzer)

## Skill Output:

**Output Type(s):** [Analysis, API Calls, Files, Shell commands, Configuration]

**Output Format:** [Markdown guidance plus JSON, HTML, PNG, or JPG artifacts from the CLI]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js 20+ and a FIGMA_ACCESS_TOKEN for Figma API access.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
