## Description: <br>
用自然语言描述数据处理需求，LLM自动生成Python/Pandas代码，帮助处理Excel/CSV数据、提取PDF内容、清洗BIM数据并构建自动化数据管道。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yesong-hue](https://clawhub.ai/user/yesong-hue) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, analysts, and construction data teams use this skill to turn natural-language data-processing requests into Python/Pandas workflows for cleaning, transforming, extracting, and exporting tabular or document-derived data. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated Python/Pandas code may transform, overwrite, or delete user data if run without review. <br>
Mitigation: Review generated code before execution, run it on copies of important files, and keep outputs in a separate directory. <br>
Risk: Third-party AI API use may transmit private, regulated, or sensitive documents outside the user's environment. <br>
Mitigation: Use local Ollama for private or regulated documents when possible, or confirm the third-party API's data transmission, retention, and policy fit before use. <br>
Risk: Scheduled automation can repeatedly apply incorrect paths or overwrite behavior. <br>
Mitigation: Avoid scheduled runs until input paths, output paths, and overwrite behavior have been explicitly reviewed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/yesong-hue/ai-llm-data-automation) <br>
- [Pandas documentation](https://pandas.pydata.org/docs/) <br>
- [Ollama installation](https://ollama.com/install.sh) <br>
- [ShadowAI API referral link](https://referer.shadowai.xyz/r/1056448) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with structured tables, Python code blocks, shell commands, and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose generated file-processing code and export options such as Excel, CSV, or JSON.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release, target metadata, SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
