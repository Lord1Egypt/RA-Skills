## Description: <br>
Build transformer fine-tuning run plans with task settings, hyperparameters, and model-card outputs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[0x-Professor](https://clawhub.ai/user/0x-Professor) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and machine learning engineers use this skill to create reproducible transformer fine-tuning run plans for Hugging Face or PyTorch workflows, including task settings, hyperparameters, evaluation cadence, and model-card skeletons. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The bundled script reads local JSON input and writes local output files, which can create or overwrite artifacts at the requested path. <br>
Mitigation: Use non-sensitive input files and choose a disposable output path before running the script. <br>
Risk: The security evidence notes that dry-run labeling should not be relied on to prevent file creation or overwrites. <br>
Mitigation: Treat dry-run output as informational and verify the destination path before execution. <br>


## Reference(s): <br>
- [Finetune Guide](references/finetune-guide.md) <br>
- [ClawHub release page](https://clawhub.ai/0x-Professor/dl-transformer-finetune) <br>
- [Publisher profile](https://clawhub.ai/user/0x-Professor) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration] <br>
**Output Format:** [JSON, Markdown, or CSV fine-tuning plan artifacts plus model-card skeleton content] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses local JSON input and writes the requested output artifact path.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
