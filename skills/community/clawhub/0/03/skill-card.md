## Description: <br>
安全的图片识别工具，支持本地和API两种模式 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nidhov01](https://clawhub.ai/user/nidhov01) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to analyze images, describe visual content, identify objects, extract text from screenshots, and batch-process image folders using either cloud API providers or a local model. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: API mode may upload private screenshots, IDs, internal documents, or other sensitive images to the selected provider. <br>
Mitigation: Use local mode for sensitive images, or confirm that sending the image to the configured provider is acceptable before using API mode. <br>
Risk: Cloud upload destinations and API configuration are not fully reviewable from the packaged files because llm_config.py is missing. <br>
Mitigation: Review or obtain llm_config.py before installing, choose the intended provider explicitly, and verify API keys, models, and endpoints. <br>
Risk: Unpinned dependencies and model downloads can change behavior over time. <br>
Mitigation: Install in a virtual environment, pin dependency versions for production use, and review downloaded model or provider behavior before deployment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/nidhov01/03) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Python dictionary or JSON-style analysis results, plus Markdown usage guidance and shell setup commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Analyzes supported image files up to 10MB and may use API providers or a local model depending on configuration.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
