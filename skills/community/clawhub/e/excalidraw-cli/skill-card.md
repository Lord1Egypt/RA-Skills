## Description:

Generate Excalidraw diagrams (flowcharts, sequences, architecture) as valid .excalidraw JSON.

This skill is ready for commercial/non-commercial use.

## Publisher:

[itspremkumar](https://clawhub.ai/user/itspremkumar)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, engineers, agents, and technical writers use this skill to create, merge, inspect, and export Excalidraw diagrams for architecture, flow, and sequence documentation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Install instructions fetch executable Python from a mutable remote branch without verification.

Mitigation: Install from the bundled reviewed excalidraw_cli.py artifact or pin and verify any remote download before execution.

Risk: Exporting SVG from Excalidraw JSON supplied by an untrusted source could carry unsafe or misleading content.

Mitigation: Export only diagrams from trusted sources, or inspect and sanitize untrusted Excalidraw JSON before conversion.

Risk: The CI verifier executes package checks and should not be run directly against untrusted packages on a sensitive host.

Mitigation: Run verification in a sandbox or disposable environment when checking third-party or untrusted skill packages.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/itspremkumar/skills/excalidraw-cli)
- [Artifact README](artifact/README.md)
- [Artifact skill definition](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with CLI commands and generated JSON, SVG, or PNG file outputs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces Excalidraw-compatible JSON diagrams and can export SVG or PNG when optional image dependencies are installed.]

## Skill Version(s):

2.0.1 (source: server release evidence; artifact frontmatter reports 2.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
