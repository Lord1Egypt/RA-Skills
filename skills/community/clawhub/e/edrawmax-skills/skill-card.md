## Description: <br>
Generate flowcharts, infographics, Gantt charts, and mind maps from natural-language prompts using EdrawMax AI APIs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wondershare-boop](https://clawhub.ai/user/wondershare-boop) <br>

### License/Terms of Use: <br>
Proprietary <br>


## Use Case: <br>
External users and developers use this skill to turn written descriptions into EdrawMax flowchart, infographic, Gantt, or mind-map outputs, then download PNG/SVG files and source code for review or editing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Diagram prompts are sent to EdrawMax's external API and may contain sensitive information. <br>
Mitigation: Avoid secrets, private customer data, and confidential plans in prompts before using the skill. <br>
Risk: Generated PNG and SVG files are downloaded and saved locally, normally under ./edrawmax_output. <br>
Mitigation: Use the bundled downloader's HTTPS and trusted-host validation, choose an appropriate output directory, and review saved files before sharing. <br>


## Reference(s): <br>
- [EdrawMax AI Skills API Reference](references/api-reference.md) <br>
- [EdrawMax AI API](https://api.edrawmax.cn/api/ai) <br>
- [ClawHub Release Page](https://clawhub.ai/wondershare-boop/edrawmax-skills) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, files, api calls, guidance] <br>
**Output Format:** [Markdown with JSON snippets, source-code blocks, image links, and local file paths] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Returns PNG/SVG diagram links and local downloaded file paths; flowcharts include Mermaid code, while infographics, Gantt charts, and mind maps include source_code.] <br>

## Skill Version(s): <br>
1.0.1 (source: ClawHub release metadata; artifact skill metadata says 2.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
