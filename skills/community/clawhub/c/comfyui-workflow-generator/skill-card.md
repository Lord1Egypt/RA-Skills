## Description: <br>
Generates ComfyUI workflows from natural language descriptions using a three-stage generation, validation, and build pipeline based on the ComfyGPT research architecture. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tianheihei002](https://clawhub.ai/user/tianheihei002) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and ComfyUI users use this skill to turn natural-language workflow requests into executable ComfyUI workflow JSON. It supports quick workflow creation while allowing inspection of generated, validated, and built stages. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can exercise local code-execution and broad file-write authority inside a ComfyUI environment. <br>
Mitigation: Review the skill before installation, run it in a trusted local ComfyUI environment, and keep catalog and workflow output paths at safe defaults. <br>
Risk: Model and tokenizer loading can expose users to untrusted model artifacts. <br>
Mitigation: Use trusted local model and tokenizer directories, and avoid HuggingFace models that require custom remote code unless the source is trusted. <br>
Risk: Debug prompt outputs may expose private workflow instructions. <br>
Mitigation: Do not share debug prompt outputs when they include private or sensitive workflow instructions. <br>
Risk: Generated workflows may use incorrect, incompatible, or missing ComfyUI nodes. <br>
Mitigation: Run the Update Node Catalog node, validate generated workflows against the local ComfyUI installation, and review outputs before execution. <br>


## Reference(s): <br>
- [ClawHub Release Page](https://clawhub.ai/tianheihei002/comfyui-workflow-generator) <br>
- [ComfyUI-WorkflowGenerator README](https://github.com/danielpflorian/ComfyUI-WorkflowGenerator) <br>
- [ComfyUI-WorkflowGenerator Wiki](https://github.com/danielpflorian/ComfyUI-WorkflowGenerator/wiki) <br>
- [ComfyGPT Paper](https://arxiv.org/abs/2503.17671) <br>
- [ComfyGPT Project Website](https://comfygpt.github.io/) <br>
- [Original ComfyGPT Repository](https://github.com/comfygpt/comfygpt) <br>
- [Original ComfyGPT Model Resources](https://huggingface.co/xiatianzs/resources/tree/main) <br>
- [Pre-Quantized WorkflowGenerator Models](https://huggingface.co/DanielPFlorian/comfyui-workflowgenerator-models) <br>
- [Sentence Transformers Embedding Model](https://huggingface.co/sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2) <br>
- [Qwen2.5-7B-Instruct Model](https://huggingface.co/Qwen/Qwen2.5-7B-Instruct) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, configuration, guidance] <br>
**Output Format:** [ComfyUI workflow JSON and status text from ComfyUI custom nodes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can optionally save generated workflow JSON files and catalog metadata in local ComfyUI directories.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
