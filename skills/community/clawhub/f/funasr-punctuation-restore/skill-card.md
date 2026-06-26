## Description: <br>
Restores Chinese and English punctuation for pasted text, single .txt files, or directories using the FunASR ct-punc model. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wangminrui2022](https://clawhub.ai/user/wangminrui2022) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to add punctuation to ASR transcripts, pasted text, individual UTF-8 .txt files, or batches of .txt files in a directory. It is limited to punctuation restoration and does not perform audio transcription, translation, or broader NLP tasks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill makes broad Python environment changes and downloads packages or model files at runtime. <br>
Mitigation: Review before installing and run it only in an isolated Python environment where package changes and network downloads are acceptable. <br>
Risk: Input text and file paths may be written to local logs during processing. <br>
Mitigation: Avoid sensitive text if local logs are unacceptable, or review and control the log directory before use. <br>
Risk: Directory mode recursively processes .txt files and creates a copied output tree. <br>
Mitigation: Run directory mode only on folders intentionally selected for punctuation restoration and verify the output path before use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wangminrui2022/funasr-punctuation-restore) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/wangminrui2022) <br>
- [FunASR ct-punc ModelScope model](https://modelscope.cn/models/damo/punc_ct-transformer_cn-en-common-vocab471067-large) <br>
- [Artifact README](artifact/README.md) <br>
- [Artifact skill instructions](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, files, shell commands, configuration, guidance] <br>
**Output Format:** [Plain text, UTF-8 .txt files, and Markdown guidance with shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Directory mode writes a sibling _punctuated mirror directory and file mode writes a _punctuated text file without modifying the original input.] <br>

## Skill Version(s): <br>
1.0.6 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
