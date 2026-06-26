## Description: <br>
使用 Genos 模型进行 DNA 序列分析。当用户提到 DNA、基因、基因组、碱基序列、ACGT 等生物信息学相关问题时使用此技能。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[flowertusi](https://clawhub.ai/user/flowertusi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and bioinformatics users use this skill to analyze DNA base sequences with the Genos-1.2B genomics model. It supports base composition statistics, GC and AT content extraction, sequence feature extraction, and next-base prediction. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Installation or first use may execute local Python and model-provided code, including model repository code loaded with trust_remote_code=True. <br>
Mitigation: Review the skill before installing, run it in a virtual environment or container, and require explicit approval before first model loading. <br>
Risk: Unpinned dependencies and model downloads can introduce supply-chain or version drift risk. <br>
Mitigation: Inspect and pin dependencies, and download Genos models only from verified official sources. <br>
Risk: The install flow may ask for a Hugging Face token when downloading models. <br>
Mitigation: Avoid entering a Hugging Face token unless necessary and use the least-privileged token available. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/flowertusi/genos-dna) <br>
- [Genos-1.2B Hugging Face model card](https://huggingface.co/ZhejiangLab/Genos-1.2B) <br>
- [Genos-1.2B ModelScope model page](https://modelscope.cn/models/zhejianglab/Genos-1.2B) <br>
- [Zhejiang Lab Genos project](https://github.com/zhejianglab/Genos) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [JSON dictionaries and Markdown guidance with shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [DNA sequence inputs are cleaned to A, C, G, T, and N before analysis; model loading requires a local Genos model path.] <br>

## Skill Version(s): <br>
0.1.1 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
