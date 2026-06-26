## Description: <br>
Use when user has/is reading a component datasheet or spec sheet to find chip parameters: pinout, voltage, I2C address, timing, register map, electrical characteristics. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[baorepo](https://clawhub.ai/user/baorepo) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and electrical engineers use this skill to extract source-cited specifications, pinouts, timing details, register information, and electrical characteristics from component datasheets. It helps answer targeted datasheet questions while requiring unsupported values to be reported as not specified with a path for obtaining the missing information. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: User-provided datasheets may contain sensitive or proprietary information. <br>
Mitigation: Use the skill only with PDFs the user is comfortable having the agent inspect, and keep analysis within the intended local workspace. <br>
Risk: The page rendering helper can write PNG output to a caller-supplied path. <br>
Mitigation: Avoid sensitive or system-level output paths when using render_page, and prefer temporary or project-local output locations. <br>
Risk: PDF parsing and rendering depend on third-party Python packages. <br>
Mitigation: Install PDF dependencies from trusted package sources, preferably in an isolated environment. <br>
Risk: Image-based PDFs and rendered diagrams can reduce extraction confidence. <br>
Mitigation: Cross-validate manufacturer, part number, pages, and table labels before using extracted values in design decisions. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/baorepo/ee-datasheet-master) <br>
- [README.md](README.md) <br>
- [PDF_STRATEGY.md](PDF_STRATEGY.md) <br>
- [TEMPLATES.md](TEMPLATES.md) <br>
- [scripts/pdf_tools.py](scripts/pdf_tools.py) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown with source-cited tables, concise analysis, and inline command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs should cite datasheet pages and tables for extracted values; missing values should be marked as not specified with an acquisition path.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
