## Description: <br>
Creates, edits, and renders Excalidraw diagrams, including flowcharts, architecture diagrams, workflows, systems, processes, and concepts, with PNG rendering and PDF export support. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[scottgl9](https://clawhub.ai/user/scottgl9) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, engineers, and technical writers use this skill to create and validate Excalidraw diagrams for software architecture, processes, workflows, and conceptual explanations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Setup uses npm package installation and Playwright browser downloads, which may matter in environments with supply-chain controls. <br>
Mitigation: Review setup.sh before installation and run setup in an isolated or policy-controlled environment when supply-chain controls are required. <br>
Risk: An older reference renderer still loads Excalidraw from a CDN. <br>
Mitigation: Use the root render_excalidraw.py renderer, which expects a local Excalidraw bundle built by setup.sh, for offline or local rendering. <br>
Risk: Generated diagram JSON can have layout issues that are not obvious until rendered. <br>
Mitigation: Render diagrams to PNG and visually inspect the output for overlap, clipping, arrow routing, and readability before delivery. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/scottgl9/excalidraw-render) <br>
- [ClawHub homepage metadata](https://clawhub.ai/skills/excalidraw-render) <br>
- [Excalidraw](https://excalidraw.com) <br>
- [Color Palette & Brand Style](references/color-palette.md) <br>
- [Element Templates](references/element-templates.md) <br>
- [Excalidraw JSON Schema](references/json-schema.md) <br>
- [Layout Rules](references/layout-rules.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files] <br>
**Output Format:** [Markdown guidance with Excalidraw JSON, shell commands, and generated diagram files such as .excalidraw, PNG, or PDF.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires local Python, uv, Node.js, npm, Playwright, and Chromium setup for rendering.] <br>

## Skill Version(s): <br>
1.0.5 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
