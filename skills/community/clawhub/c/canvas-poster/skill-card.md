## Description: <br>
Canvas Poster is a server-side poster and dashboard image generator that uses a declarative JSON section DSL to produce PNG reports with KPI cards, charts, tables, and suggestion blocks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhaoweismydd-cloud](https://clawhub.ai/user/zhaoweismydd-cloud) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and analysts use this skill to generate long-form business, finance, investment, and operational dashboard images from structured data without a browser or headless Chrome. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can write generated PNG images to caller-provided output paths. <br>
Mitigation: Use explicit safe output paths and avoid allowing untrusted input to choose filenames or directories. <br>
Risk: Generated business or financial posters may contain incorrect or misleading content if the source data or prompt is wrong. <br>
Mitigation: Review generated reports before sharing them externally. <br>


## Reference(s): <br>
- [Canvas Poster on ClawHub](https://clawhub.ai/zhaoweismydd-cloud/canvas-poster) <br>
- [README.md](README.md) <br>
- [@napi-rs/canvas](https://github.com/nicknisi/napi-rs-canvas) <br>
- [Claude Code](https://claude.ai/claude-code) <br>


## Skill Output: <br>
**Output Type(s):** [code, shell commands, configuration, guidance, files] <br>
**Output Format:** [Markdown with inline JavaScript and shell examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local PNG poster files when an output path is provided.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
