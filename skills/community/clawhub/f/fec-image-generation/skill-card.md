## Description: <br>
Image Generation helps agents generate and edit visual assets, deterministic diagrams, themed HTML/SVG technical diagrams, and exported PNGs with bounded QA repair loops. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bovinphang](https://clawhub.ai/user/bovinphang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, designers, and agents use this skill to choose an appropriate visual generation route, create editable diagram or image sources, export deliverables, and report visual QA findings. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Interactive diagram sessions can expose sensitive diagram labels through the local server or persisted session files. <br>
Mitigation: Keep the server bound to 127.0.0.1, use unique session IDs, avoid secrets in diagram labels, and clear temporary session files when content is sensitive. <br>
Risk: Generated diagrams or images can contain incorrect labels, formulas, brand details, or misleading visual structure. <br>
Mitigation: Retain editable sources, run the documented PNG QA checks when available, and manually verify proper nouns, formulas, brand specifications, labels, and diagram connections before delivery. <br>
Risk: PNG/JPG export depends on local browser or converter availability and may fail or produce incomplete raster output. <br>
Mitigation: Export SVG or browser-ready HTML when raster export is unavailable, and inspect exported PNG/JPG files before using them as final deliverables. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/bovinphang/skills/fec-image-generation) <br>
- [README](README.md) <br>
- [Artifact Routing](references/artifact-routing.md) <br>
- [Diagram Workflows](references/diagram-workflows.md) <br>
- [HTML Technical Diagrams](references/html-technical-diagrams.md) <br>
- [PNG QA And Autofix](references/png-qa-autofix.md) <br>
- [Interactive Diagram Asset](assets/interactive-diagram.html) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JSON, HTML/SVG source, shell command examples, and optional exported image files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce editable diagram source, PNG/SVG/JPG exports, browser-ready HTML diagrams, prompts, and QA notes depending on the selected route and available host tools.] <br>

## Skill Version(s): <br>
2.8.0 (source: package.json, artifact metadata, evidence release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
