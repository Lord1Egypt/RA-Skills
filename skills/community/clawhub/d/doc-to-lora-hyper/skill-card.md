## Description: <br>
Doc-to-LoRA internalizes a document into Gemma 2 2B by generating LoRA adapter weights so an agent can answer questions without putting the document in the prompt. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Manojbhat09](https://clawhub.ai/user/Manojbhat09) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users on Apple Silicon Macs use this skill to internalize document text into a local Doc-to-LoRA adapter and query it with PyTorch or MLX. It is best suited for factual document recall rather than deep multi-hop reasoning. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Checkpoint loading can deserialize Python objects from model files. <br>
Mitigation: Load checkpoints only from trusted sources, avoid arbitrary checkpoint paths, and verify or pin downloaded model revisions where possible. <br>
Risk: Setup and model download steps depend on external repositories, Python packages, and a HuggingFace token. <br>
Mitigation: Install only from a trusted doc-to-lora repository, review dependency changes before setup, and use a limited HuggingFace token. <br>
Risk: Generated adapters and result files may preserve information from sensitive input documents. <br>
Mitigation: Handle adapters and JSON/text outputs with the same access controls and retention rules as the source documents. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/Manojbhat09/doc-to-lora-hyper) <br>
- [Doc-to-LoRA Architecture](references/ARCHITECTURE.md) <br>
- [Doc-to-LoRA paper](https://arxiv.org/abs/2602.15902) <br>
- [Gemma 2 2B Instruct base model](https://huggingface.co/google/gemma-2-2b-it) <br>
- [SakanaAI Doc-to-LoRA weights](https://huggingface.co/SakanaAI/doc-to-lora) <br>
- [uv package manager](https://docs.astral.sh/uv/) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, Text, JSON, Files] <br>
**Output Format:** [Markdown guidance with bash examples; scripts emit plain-text answers, optional JSON result files, and adapter directories.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Default answer generation is capped at 256 new tokens unless changed by the user; generated adapters and result files may contain sensitive document-derived information.] <br>

## Skill Version(s): <br>
1.2.0 (source: server release and skill metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
