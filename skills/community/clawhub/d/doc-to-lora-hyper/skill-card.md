## Description:

Doc-to-LoRA internalizes a document into Gemma 2 2B by generating a LoRA adapter so an agent can answer questions about the document without including it in the prompt.

This skill is ready for commercial/non-commercial use.

## Publisher:

[manojbhat09](https://clawhub.ai/user/manojbhat09)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and AI agent users use this skill on Apple Silicon Macs to internalize supplied documents or text into Doc-to-LoRA adapters and query them through PyTorch or MLX workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Checkpoint loading can execute unsafe Python objects when an untrusted Doc-to-LoRA checkpoint is used.

Mitigation: Load only official or hash-verified checkpoints, and keep the default SakanaAI/doc-to-lora source unless the replacement is trusted.

Risk: Setup runs local repository installation logic and installs dependencies, which can introduce code-execution risk in an untrusted clone.

Mitigation: Install only in a trusted Doc-to-LoRA repository clone, inspect install_mac.sh before setup, and prefer pinned or locked dependencies.

Risk: HF_TOKEN is required for gated Gemma access and is a sensitive credential.

Mitigation: Use a minimally scoped Hugging Face token, keep it out of logs and shared shell history, and remove it from the environment when setup is complete.

Risk: The unpinned npx install path can fetch code whose exact source revision is not fixed.

Mitigation: Avoid the npx path unless the installer and source revision are trusted.

## Reference(s):

- [Doc-to-LoRA paper](https://arxiv.org/abs/2602.15902)
- [Doc-to-LoRA architecture](references/ARCHITECTURE.md)
- [Gemma 2 2B base model](https://huggingface.co/google/gemma-2-2b-it)
- [SakanaAI Doc-to-LoRA weights](https://huggingface.co/SakanaAI/doc-to-lora)
- [uv package manager](https://docs.astral.sh/uv/)
- [ClawHub skill page](https://clawhub.ai/manojbhat09/skills/doc-to-lora-hyper)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with bash commands; script outputs are plain text answers or optional JSON result files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Targets macOS on Apple Silicon, requires python3, uv, HF_TOKEN, local Doc-to-LoRA repository files, and trusted model checkpoints.]

## Skill Version(s):

1.2.0 (source: server release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
