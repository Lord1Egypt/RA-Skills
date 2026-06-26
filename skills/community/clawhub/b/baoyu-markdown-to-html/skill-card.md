## Description: <br>
Converts Markdown to styled HTML with WeChat-compatible themes, including support for code highlighting, math, Mermaid rendered through headless Chrome, PlantUML, footnotes, alerts, infographics, and optional bottom citations for external links. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jimliu](https://clawhub.ai/user/jimliu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, writers, and content operators use this skill to convert Markdown articles into styled HTML suitable for WeChat Official Account and similar publishing workflows. It can preserve common Markdown features, render supported diagrams, apply themes, and optionally move ordinary external links into a bottom citation section. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The converter reads the selected Markdown file and referenced local images. <br>
Mitigation: Run it only on documents and referenced files that are intended for conversion and review the generated HTML before publishing. <br>
Risk: Remote images referenced in Markdown may be fetched by the rendering library. <br>
Mitigation: Review image URLs before conversion or use local copies when network fetching is not acceptable. <br>
Risk: Mermaid rendering may launch headless Chrome and create cached PNG files. <br>
Mitigation: Use trusted Mermaid content, keep the browser runtime updated, or disable Mermaid rendering with the skill's no-Mermaid option when browser rendering is not desired. <br>
Risk: The skill writes HTML, backup files, and diagram cache files next to the input. <br>
Mitigation: Run the converter in an appropriate working directory and check output, backup, and cache paths before sharing or committing files. <br>


## Reference(s): <br>
- [Project homepage](https://github.com/JimLiu/baoyu-skills#baoyu-markdown-to-html) <br>
- [ClawHub skill listing](https://clawhub.ai/jimliu/baoyu-markdown-to-html) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell command examples; the invoked converter writes HTML files and emits JSON execution results.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces an HTML file beside the input Markdown, may create timestamped HTML backups, may cache Mermaid PNG images, and reports paths and image metadata as JSON.] <br>

## Skill Version(s): <br>
1.117.3 (source: SKILL.md frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
