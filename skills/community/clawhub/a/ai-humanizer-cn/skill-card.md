## Description: <br>
中文 AI 文本优化技能，支持多种 AI 模型（OpenAI/Anthropic/阿里），去除 AI 痕迹，保持专业性。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[pengong101](https://clawhub.ai/user/pengong101) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers can use this skill to rewrite AI-generated Chinese and English text into more natural styles, batch-process text files, and optimize code comments for selected programming languages. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Input text may be processed by configured third-party AI providers despite artifact documentation also claiming local processing. <br>
Mitigation: Avoid confidential, regulated, or proprietary text unless third-party processing is intended and approved. <br>
Risk: Batch processing can send or transform more files than intended if paths are broad. <br>
Mitigation: Keep batch paths narrow and review selected input and output directories before running the skill. <br>
Risk: Configured provider credentials may have more access than this task requires. <br>
Mitigation: Use restricted API keys and rotate or revoke them after testing when appropriate. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/pengong101/ai-humanizer-cn) <br>
- [Publisher profile](https://clawhub.ai/user/pengong101) <br>
- [Documentation link listed in artifact](https://ai-humanizer-cn.readthedocs.io/) <br>
- [Package link listed in artifact](https://pypi.org/project/ai-humanizer-cn/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with Python and shell command examples; runtime output is rewritten text or code.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May use configured API keys and batch paths when provider-backed processing is enabled.] <br>

## Skill Version(s): <br>
5.0.0 (source: server release evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
