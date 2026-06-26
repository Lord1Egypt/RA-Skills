## Description: <br>
稿定设计对话式设计工具。支持搜索模板、选择模板、编辑文案、预览、导出设计。覆盖海报、PPT、电商主图、名片等全场景。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gezilinll](https://clawhub.ai/user/gezilinll) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
OpenClaw users use this skill to search Gaoding templates with natural language, preview choices, edit text, and export finished design files for posters, presentations, ecommerce images, business cards, and similar Chinese-language design workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses a real Gaoding account and stores login state locally. <br>
Mitigation: Use a dedicated Gaoding account where possible, protect .env and cookies.json, and never commit or share those files. <br>
Risk: Exported design files and screenshots may contain user-provided or account-derived content. <br>
Mitigation: Store outputs only on trusted machines and delete exported files and screenshots when they are no longer needed. <br>
Risk: Browser automation depends on Gaoding website behavior and may fail if the site changes. <br>
Mitigation: Run the included smoke test after installation or updates, and prefer the search workflow if editing or export automation fails. <br>


## Reference(s): <br>
- [Gaoding Design Skill Page](https://clawhub.ai/gezilinll/gaoding-design) <br>
- [Gaoding Design](https://www.gaoding.com) <br>
- [OpenClaw](https://github.com/nicepkg/openclaw) <br>
- [User Guide](docs/user-guide.md) <br>
- [Troubleshooting](docs/troubleshooting.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON tool outputs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Search returns template metadata and a screenshot path; export returns a generated design file path.] <br>

## Skill Version(s): <br>
2.0.0 (source: SKILL.md frontmatter, package.json, ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
