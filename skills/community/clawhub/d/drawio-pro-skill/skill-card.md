## Description:

Helps agents create, validate, and export draw.io diagrams for architecture, UML, ERD, flowcharts, network topology, infrastructure, and other technical visualizations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[agents365-ai](https://clawhub.ai/user/agents365-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to produce polished, editable diagrams and related exports for software architecture, infrastructure, data models, processes, and technical explanations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill runs local draw.io and Python tooling over user-selected files.

Mitigation: Install and run it only in workspaces where local file processing is acceptable, and review generated commands before execution.

Risk: Generated HTML animation helpers have disclosed title escaping bugs for attacker-controlled filenames or repository directory names.

Mitigation: Avoid attacker-controlled filenames and repository directory names with those helpers until the escaping issue is fixed.

Risk: Logo lookup behavior can use CDN-hosted assets.

Mitigation: Use embedded or local assets when external CDN requests are not acceptable.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/agents365-ai/skills/drawio-pro-skill)
- [Publisher Profile](https://clawhub.ai/user/agents365-ai)
- [Toolbox Reference](artifact/references/toolbox.md)
- [Diagram Type Presets](artifact/references/diagram-types.md)
- [XML Authoring Reference](artifact/references/xml-authoring.md)
- [Auto-layout Reference](artifact/references/autolayout.md)
- [Troubleshooting Reference](artifact/references/troubleshooting.md)
- [Shape Index Notice](artifact/data/SHAPE-INDEX-NOTICE.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with draw.io XML, JSON inputs, and shell commands as needed]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce editable .drawio files and exported PNG, SVG, PDF, JPG, PPTX, Mermaid, or HTML artifacts when supporting tools are available.]

## Skill Version(s):

1.34.0 (source: server release evidence and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
