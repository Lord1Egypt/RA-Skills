## Description: <br>
An AI skill for OpenClaw that generates professional diagrams from natural language descriptions using EdrawMax AI APIs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xkWeiMeng](https://clawhub.ai/user/xkWeiMeng) <br>

### License/Terms of Use: <br>
Proprietary Software License <br>


## Use Case: <br>
Developers, knowledge workers, and diagram authors use this skill to turn natural-language process, timeline, data, or knowledge-structure descriptions into flowcharts, infographics, Gantt charts, or mind maps. The skill calls EdrawMax AI APIs, downloads generated PNG and SVG files locally, and returns editable diagram source code. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Diagram prompts are sent to EdrawMax AI APIs and may contain sensitive process, business, or regulated information. <br>
Mitigation: Avoid secrets, confidential plans, regulated data, and sensitive internal process details in prompts. <br>
Risk: The downloader weakens HTTPS verification before saving generated PNG and SVG files locally. <br>
Mitigation: Review or fix the downloader to keep HTTPS verification enabled and restrict downloads to expected EdrawMax or OSS domains before relying on generated files. <br>
Risk: Generated SVG files can carry active or unsafe content if a download source is not trusted. <br>
Mitigation: Inspect generated SVGs and open them in controlled viewers until the downloader verifies trusted HTTPS sources. <br>


## Reference(s): <br>
- [EdrawMax AI Skills API Reference](references/api-reference.md) <br>
- [EdrawMax AI API Base URL](https://api.edrawmax.cn/api/ai) <br>
- [ClawHub skill page](https://clawhub.ai/xkWeiMeng/edrawmax-diagram) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, files, API calls, guidance] <br>
**Output Format:** [Markdown guidance with JSON API examples, local PNG/SVG file paths, and diagram source code] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Downloads generated PNG and SVG assets to local disk and reports paths as JSON from the helper script.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
