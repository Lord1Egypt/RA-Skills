## Description:

Generate hand-drawn style diagrams, flowcharts, and architecture diagrams as PNG images from Excalidraw JSON.

This skill is ready for commercial/non-commercial use.

## Publisher:

[erdmannsilva](https://clawhub.ai/user/erdmannsilva)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to create hand-drawn style flowcharts, architecture diagrams, and related visuals from structured Excalidraw JSON and render them as PNG images.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup depends on npm package installation and external font downloads, which can introduce dependency and download hygiene risk.

Mitigation: Review dependencies before installation, prefer verified downloads, and update vulnerable packages before production use.

Risk: The documented workflow writes diagram inputs and outputs under /tmp, which may expose sensitive diagram content in shared environments.

Mitigation: Use private temporary directories or another restricted workspace when diagrams may contain sensitive information.

Risk: The security summary recommends review before installing in a trusted environment.

Mitigation: Run setup and rendering from an unprivileged account and review the skill before deployment.

## Reference(s):

- [Excalidraw Element Schema Reference](references/element-schema.md)

## Skill Output:

**Output Type(s):** [Code, Shell commands, Files, Guidance]

**Output Format:** [Excalidraw JSON rendered to PNG, with concise text or Markdown guidance when needed]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The renderer accepts an .excalidraw or JSON input file and writes a PNG output file.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
