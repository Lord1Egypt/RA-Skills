## Description: <br>
Restrained information visualization skill pack for AI agents that turns briefs into Mermaid, ASCII/termaid, self-contained HTML, Python, draw.io, Obsidian Canvas, and Three.js archviz outputs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[archsueh](https://clawhub.ai/user/archsueh) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, designers, technical writers, and agent operators use this skill to turn visualization briefs into restrained diagrams, charts, editable handoff guidance, and 3D architectural visualizations with explicit design dials, palettes, validation checks, and fallbacks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated HTML may load Chart.js, Three.js, or animejs from third-party CDNs. <br>
Mitigation: Review generated HTML before opening it, and vendor or pin browser dependencies for offline or sensitive environments. <br>
Risk: The artifact includes self-evolution guidance that can modify installed skill files. <br>
Mitigation: Require explicit approval before edits to installed skill files, or disable the self-evolution section for controlled deployments. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/archsueh/archviz-skills) <br>
- [README](README.md) <br>
- [Design system](DESIGN.md) <br>
- [Scene contract](references/scene-contract.md) <br>
- [Validation checklist](references/validation-checklist.md) <br>
- [termaid terminal routing](references/termaid-routing.md) <br>
- [draw.io output mode](references/drawio-output-mode.md) <br>
- [Dark mode tokens](references/dark-mode-tokens.md) <br>
- [Editorial parchment language](references/editorial-parchment-language.md) <br>
- [Gantt rules](references/gantt-rules.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown, Mermaid, ASCII text, self-contained HTML, Python code, draw.io guidance, and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include generated files/templates and validation or fallback guidance; generated HTML may load third-party browser scripts from CDNs.] <br>

## Skill Version(s): <br>
1.1.2 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
