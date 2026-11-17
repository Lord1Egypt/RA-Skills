## Description:

使用 Genos 模型进行 DNA 序列分析。当用户提到 DNA、基因、基因组、碱基序列、ACGT 等生物信息学相关问题时使用此技能。

This skill is ready for commercial/non-commercial use.

## Publisher:

[flowertusi](https://clawhub.ai/user/flowertusi)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, bioinformatics practitioners, and genomics researchers use this skill to analyze DNA base sequences, compute sequence statistics, extract features, and request next-base predictions with a local Genos model.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can execute downloaded third-party ML model code locally.

Mitigation: Run it in a clean virtual environment or container, verify model artifacts and sources before use, and avoid running the installer or model with administrator/root privileges.

Risk: The installer can handle Hugging Face tokens without strong safeguards.

Mitigation: Avoid entering broad or long-lived Hugging Face tokens into install.sh; use least-privilege, short-lived credentials in trusted environments only.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/flowertusi/skills/genos-dna)
- [Genos-1.2B Hugging Face model card](https://huggingface.co/ZhejiangLab/Genos-1.2B)
- [Genos ModelScope model page](https://modelscope.cn/models/zhejianglab/Genos-1.2B)
- [ZhejiangLab Genos repository](https://github.com/zhejianglab/Genos)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with Python and shell code blocks; runtime functions return JSON-compatible dictionaries.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include sequence length, base composition, GC and AT content, model metadata, and next-base prediction probabilities.]

## Skill Version(s):

0.1.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
