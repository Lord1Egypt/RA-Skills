## Description: <br>
Displays Chinese text with pinyin pronunciation in a two-line format for children learning Chinese and pinyin. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[guytogay](https://clawhub.ai/user/guytogay) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and language-learning assistants use this skill to keep Chinese-learning conversations in a paired pinyin-and-Hanzi display format. It is intended for children learning Chinese pronunciation and for contexts where pinyin helps literacy learning. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill's child-mode formatting continues until an explicit exit phrase is used. <br>
Mitigation: Enable it only for conversations that need pinyin display, and use one of the documented exit phrases before returning to normal formatting. <br>
Risk: Two-line pinyin output can become misaligned for multi-codepoint emoji, rare characters, or incorrect polyphonic readings. <br>
Mitigation: Use the included validation script for generated examples, prefer simple emoji in child-facing output, and review phrase overrides for words that need precise pronunciation. <br>
Risk: The local helper depends on the npm package pinyin-pro. <br>
Mitigation: Review the dependency against your npm policy before installation and install from the recorded package metadata when reproducing this release. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/guytogay/chinese-pinyin-display) <br>
- [pinyin-pro 3.28.0 package artifact](https://registry.npmjs.org/pinyin-pro/-/pinyin-pro-3.28.0.tgz) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Two-line plain text output with a pinyin line followed by a Chinese character line, plus Markdown guidance and shell commands for setup or validation.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Output should preserve matching punctuation, spacing, and character positions across the pinyin and Chinese lines.] <br>

## Skill Version(s): <br>
1.2.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
