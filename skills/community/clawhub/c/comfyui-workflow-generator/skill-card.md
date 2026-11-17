## Description:

Comfyui Workflow Generator helps users generate ComfyUI workflow JSON from natural-language descriptions through a generation, validation, and build pipeline.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tianheihei002](https://clawhub.ai/user/tianheihei002)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and ComfyUI users use this skill to turn natural-language workflow requests into executable ComfyUI workflow JSON. It supports a three-stage process that generates a workflow diagram, validates node names against the local catalog, and builds the final graph.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unsafe model-loading defaults can expose users to untrusted model or tokenizer behavior.

Mitigation: Use trusted local model and tokenizer files, prefer known GGUF assets, and avoid Hugging Face model directories that require custom code.

Risk: Broad catalog and output path controls can write workflow or catalog files to unintended locations.

Mitigation: Keep catalog and output paths at safe defaults, and review filename_prefix and catalog_directory values before enabling workflow file output.

Risk: Generated workflows can include outdated, incompatible, or incorrect ComfyUI nodes.

Mitigation: Run the Update Node Catalog node first, validate generated node names against the local installation, and inspect workflow JSON before use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/tianheihei002/skills/comfyui-workflow-generator)
- [ComfyGPT paper](https://arxiv.org/abs/2503.17671)
- [ComfyGPT project website](https://comfygpt.github.io/)
- [ComfyGPT original repository](https://github.com/comfygpt/comfygpt)
- [WorkflowGenerator model resources](https://huggingface.co/xiatianzs/resources/tree/main)
- [Embedding model](https://huggingface.co/sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2)
- [NodeValidator model](https://huggingface.co/Qwen/Qwen2.5-7B-Instruct)
- [Pre-quantized GGUF models](https://huggingface.co/DanielPFlorian/comfyui-workflowgenerator-models)
- [ComfyUI-WorkflowGenerator documentation](https://github.com/danielpflorian/ComfyUI-WorkflowGenerator/wiki)

## Skill Output:

**Output Type(s):** [text, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON workflow content and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated workflows should be reviewed in ComfyUI before use.]

## Skill Version(s):

1.0.0 (source: SKILL.md frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
