## Description:

A restrained information visualization skill pack for AI agents that routes briefs into Mermaid, ASCII or termaid, self-contained HTML, Python visualizations, Obsidian Canvas, draw.io guidance, or Three.js architectural visualization outputs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[archsueh](https://clawhub.ai/user/archsueh)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, designers, educators, and technical teams use this skill to create concise diagrams, charts, architectural visualizations, editable diagram handoffs, and text-first visual artifacts from a user brief.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated HTML can load scripts from jsDelivr and execute remote code when opened or hosted.

Mitigation: Review generated HTML before opening or hosting it, and pin or vendor dependencies where possible.

Risk: Python visualization modes may require local dependencies and script execution.

Mitigation: Use a dedicated virtual environment and review generated scripts before running them.

Risk: Self-evolution or maintenance workflows can modify installed skill files.

Mitigation: Allow installed skill edits only when explicitly requested, then review diffs before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/archsueh/skills/archviz-skills)
- [README](artifact/README.md)
- [Design system](artifact/DESIGN.md)
- [Validation checklist](artifact/references/validation-checklist.md)
- [Termaid routing](artifact/references/termaid-routing.md)
- [Draw.io output mode](artifact/references/drawio-output-mode.md)
- [Scene contract](artifact/references/scene-contract.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown, Mermaid or ASCII diagrams, self-contained HTML, Python scripts, draw.io guidance, and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs are brief-driven and may include terminal fallbacks, CDN-backed HTML visualization templates, or Python dependency guidance depending on the selected mode.]

## Skill Version(s):

1.1.2 (source: server release evidence; artifact frontmatter reports 0.1.7)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
