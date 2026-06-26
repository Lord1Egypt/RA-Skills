## Description: <br>
Turns articles or notes into mobile-readable HTML infographics with a visual style selected for the source content. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[partigle](https://clawhub.ai/user/partigle) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, content creators, and developers use this skill to condense articles, posts, or notes into self-contained HTML infographics and screenshot-ready visual assets. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill generates local HTML files and runs an included post-processing script against those files. <br>
Mitigation: Review generated HTML before running post-processing, execute only in a trusted workspace, and inspect script changes before deployment. <br>
Risk: Generated or template HTML may load external web fonts, which can disclose request metadata to third-party font providers. <br>
Mitigation: Remove external font imports or replace them with local fonts for private or sensitive content. <br>
Risk: The screenshot workflow may start a temporary local HTTP server for generated output. <br>
Mitigation: Bind the server to 127.0.0.1 where possible, serve only the output directory, and stop the server after capture. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/partigle/article-to-html) <br>
- [Quick Start](docs/01-快速开始.md) <br>
- [Design Specification](docs/02-设计规范.md) <br>
- [Technical Baseline](rules/01-技术底线.md) <br>
- [Screenshot Workflow](rules/02-截图流程.md) <br>
- [Style Inspiration](rules/03-风格灵感.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, code, files, shell commands, guidance] <br>
**Output Format:** [Self-contained HTML, Markdown guidance, and optional PNG screenshot output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated HTML is post-processed by the included shell and Node.js scripts before screenshot delivery.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
