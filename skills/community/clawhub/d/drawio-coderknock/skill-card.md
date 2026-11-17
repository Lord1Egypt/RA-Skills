## Description:

Generates editable Draw.io architecture and flowchart files from preset templates or short descriptions, detects a local Draw.io installation, and can open the generated diagram for editing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[coder-knock](https://clawhub.ai/user/coder-knock)

### License/Terms of Use:

MIT

## Use Case:

Developers and engineers use this skill to generate editable Draw.io diagrams for ecommerce systems, CEX exchange architecture, login flows, order flows, approval flows, and generic process documentation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Local file handling is under-scoped when generating diagram files.

Mitigation: Run the skill in a dedicated workspace and review generated output paths before execution.

Risk: Untrusted descriptions or template names may affect generated file names or diagram content.

Mitigation: Use trusted inputs, enforce an allowlist for template values, and ensure XML attribute escaping before broader deployment.

Risk: The skill may auto-open generated files in a local Draw.io installation.

Mitigation: Require explicit confirmation before allowing an agent to open local applications or generated files.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/coder-knock/skills/drawio-coderknock)
- [Publisher profile](https://clawhub.ai/user/coder-knock)
- [Draw.io desktop releases](https://github.com/jgraph/drawio-desktop/releases)
- [diagrams.net online editor](https://app.diagrams.net/)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance, Files]

**Output Format:** [Markdown guidance with Python commands and generated .drawio or .mmd files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create local diagram files in the selected workspace and may attempt to open Draw.io when installed.]

## Skill Version(s):

1.0.0 (source: server release, package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
