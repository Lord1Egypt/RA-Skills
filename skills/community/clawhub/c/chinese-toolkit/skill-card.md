## Description:

为OpenClaw提供中文文本处理、翻译、OCR、语音识别等功能的综合工具包，支持中文分词、拼音转换、中英文翻译、关键词提取和文本分析。

This skill is ready for commercial/non-commercial use.

## Publisher:

[utopia013-droid](https://clawhub.ai/user/utopia013-droid)

### License/Terms of Use:

MIT

## Use Case:

Developers and OpenClaw users use this skill to process Chinese-language content through segmentation, pinyin conversion, translation, keyword extraction, summarization, OCR-oriented workflows, and text analysis. It is intended for agents that need Chinese text utilities exposed through Python, command-line, or OpenClaw-style calls.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The installer can download and run code that is outside the reviewed package contents.

Mitigation: Do not run install.sh until it is changed to install only reviewed, pinned package contents; install dependencies in an isolated environment after manual review.

Risk: The package includes out-of-scope release, inbox, forum, and documentation-validator materials unrelated to Chinese text tooling.

Mitigation: Remove or isolate those materials before deployment and limit agent access to the Chinese text-processing files required for the intended workflow.

Risk: Bundled publishing, reset, and credential-oriented guidance could expose accounts or alter repositories if followed during normal use.

Mitigation: Do not provide mailbox credentials or execute bundled publishing and reset commands as part of using the skill.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/utopia013-droid/skills/chinese-toolkit)
- [Publisher profile](https://clawhub.ai/user/utopia013-droid)
- [jieba Chinese text segmentation](https://github.com/fxsjy/jieba)
- [pypinyin](https://github.com/mozillazg/python-pinyin)
- [OpenCC](https://github.com/BYVoid/OpenCC)
- [requests](https://github.com/psf/requests)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with Python, shell, and JSON examples; tool calls return text or JSON-like dictionaries.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Python 3 and pip; translation, OCR, and speech workflows may require API credentials or optional system packages.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
