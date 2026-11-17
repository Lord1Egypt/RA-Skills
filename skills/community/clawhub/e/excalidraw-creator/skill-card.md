## Description:

Create hand-drawn style Excalidraw diagrams, flowcharts, and architecture visuals as PNG images.

This skill is ready for commercial/non-commercial use.

## Publisher:

[plgonzalezrx8](https://clawhub.ai/user/plgonzalezrx8)

### License/Terms of Use:


## Use Case:

Developers and agents use this skill to create hand-drawn style diagrams, flowcharts, and architecture visuals by producing Excalidraw-compatible JSON and rendering it to PNG images.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup installs npm packages and downloads font assets before local rendering.

Mitigation: Run setup in an isolated environment, review the package lock file, and avoid elevated privileges.

Risk: Downloaded font assets are not hash-verified by the setup script.

Mitigation: Verify downloaded assets independently or provide trusted local font files before production use.

Risk: Shared-machine setup has predictable /tmp usage during Cascadia font extraction.

Mitigation: Run setup as an unprivileged user in a controlled workspace or use a revised setup flow with safer temporary paths.

## Reference(s):

- [Excalidraw Element Schema Reference](references/element-schema.md)
- [ClawHub skill page](https://clawhub.ai/plgonzalezrx8/skills/excalidraw-creator)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, files]

**Output Format:** [Markdown guidance with JSON examples and shell commands; PNG image files from rendered Excalidraw JSON.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The renderer accepts an .excalidraw JSON file or standard input and writes a PNG output file.]

## Skill Version(s):

1.0.0 (source: release evidence, scripts/package.json, scripts/package-lock.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
