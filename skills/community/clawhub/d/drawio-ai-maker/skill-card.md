## Description: <br>
Converts natural-language descriptions or docx, pdf, and txt documents into editable draw.io XML diagrams as .drawio files. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wuliwenjing](https://clawhub.ai/user/wuliwenjing) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and technical users use this skill to turn process, architecture, sequence, network, hierarchy, function, and deployment descriptions into draw.io diagrams that can be reviewed and edited in diagrams.net. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill writes generated .drawio files to a local output directory that may be outside a bounded workspace. <br>
Mitigation: Set and verify DRAWIO_OUTPUT_DIR or the output-dir option before use, and avoid sensitive folders. <br>
Risk: The documented confirmation step may not be enforced consistently before saving generated output. <br>
Mitigation: Review the generated diagram content and destination before permitting any save operation. <br>
Risk: Generated diagrams may have imperfect spacing, routing, or layout. <br>
Mitigation: Open the .drawio file in diagrams.net and manually review or adjust the diagram before sharing or using it. <br>


## Reference(s): <br>
- [draw.io XML Format Reference](references/drawio-xml-spec.md) <br>
- [diagrams.net draw.io editor](https://app.diagrams.net) <br>
- [ClawHub skill page](https://clawhub.ai/wuliwenjing/drawio-ai-maker) <br>
- [Publisher profile](https://clawhub.ai/user/wuliwenjing) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Code, Shell commands, Files, Guidance] <br>
**Output Format:** [Markdown instructions, structured JSON, shell commands, and generated .drawio XML files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated files are written to a local output directory controlled by DRAWIO_OUTPUT_DIR or command-line options.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
