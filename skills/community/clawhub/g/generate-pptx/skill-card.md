## Description: <br>
Clarifies presentation requirements, confirms a slide-by-slide plan, generates SVG slides, and packages them into a PPTX file. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[likegakki](https://clawhub.ai/user/likegakki) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees, external users, developers, and presentation authors use this skill to turn briefs, outlines, long-form copy, or existing SVG slides into structured presentation plans and downloadable PPTX files. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may create or reuse a Python virtual environment and install python-pptx from pip. <br>
Mitigation: Run it in a dedicated virtual environment or container, or preinstall the dependency before using the PPTX packaging scripts. <br>


## Reference(s): <br>
- [Skill page](https://clawhub.ai/likegakki/generate-pptx) <br>
- [Gazee Glacier visual preset](references/presets/gazee-glacier.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, files] <br>
**Output Format:** [Markdown guidance, JSON slide arrays containing SVG strings, shell commands, intermediate SVG files, and PPTX files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated slides are expected to use 16:9 SVG with a 1280x720 viewBox before packaging into PPTX.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
