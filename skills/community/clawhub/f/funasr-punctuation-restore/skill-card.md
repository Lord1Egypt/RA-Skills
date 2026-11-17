## Description:

Restores Chinese and English punctuation for pasted text, a single .txt file, or a directory of text files using the FunASR ct-punc model.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wangminrui2022](https://clawhub.ai/user/wangminrui2022)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agent operators use this skill to clean up ASR transcripts or unpunctuated text by adding punctuation to direct text input, one text file, or every .txt file in a directory while preserving the original input.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill downloads and installs Python packages at runtime, including unpinned packages.

Mitigation: Run it in an isolated environment and review dependency installation behavior before normal use.

Risk: The skill creates persistent local artifacts such as a virtual environment, cached model files, logs, and punctuated output files.

Mitigation: Use a workspace without sensitive credentials, review output and log locations, and avoid confidential text until logging behavior is addressed.

Risk: The scanner notes unrelated audio dependencies and import-time package repair logic for a punctuation-only skill.

Mitigation: Review or remove the unrelated dependencies and package repair logic before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wangminrui2022/skills/funasr-punctuation-restore)
- [FunASR ct-punc ModelScope model](https://modelscope.cn/models/damo/punc_ct-transformer_cn-en-common-vocab471067-large)

## Skill Output:

**Output Type(s):** [text, files, shell commands, guidance]

**Output Format:** [Plain text output, UTF-8 .txt files, and Markdown command guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Directory mode writes a sibling _punctuated directory and file mode writes a _punctuated.txt output without modifying the original input.]

## Skill Version(s):

1.0.8 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
