## Description: <br>
Generates flowcharts, infographics, Gantt charts, and mind maps from natural language descriptions using EdrawMax AI APIs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xkWeiMeng](https://clawhub.ai/user/xkWeiMeng) <br>

### License/Terms of Use: <br>
Proprietary <br>


## Use Case: <br>
Developers, employees, and external users can use this skill to turn written process, project, knowledge, or data descriptions into editable diagram outputs through EdrawMax AI APIs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Diagram descriptions are sent to EdrawMax AI APIs. <br>
Mitigation: Avoid sending sensitive or confidential prompts unless the user has approved that disclosure. <br>
Risk: The required downloader saves remote files while TLS certificate verification is disabled. <br>
Mitigation: Review returned URLs before downloading and prefer expected EdrawMax or diagram-hosting URLs until the downloader enforces normal HTTPS verification. <br>
Risk: Downloaded SVG files may contain unsafe or unexpected content. <br>
Mitigation: Open SVG outputs cautiously, inspect them when possible, and avoid treating downloaded files as trusted without review. <br>


## Reference(s): <br>
- [EdrawMax AI API Reference](artifact/references/api-reference.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/xkWeiMeng/build-diagram) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Code, Shell commands, Files, Guidance] <br>
**Output Format:** [Markdown response with local file paths, diagram source code, and JSON downloader output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May save PNG and SVG files locally; flowcharts return Mermaid code, while infographics, Gantt charts, and mind maps return source_code.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
