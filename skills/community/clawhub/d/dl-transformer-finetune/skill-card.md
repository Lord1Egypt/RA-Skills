## Description:

Build transformer fine-tuning run plans with task settings, hyperparameters, and model-card outputs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[0x-professor](https://clawhub.ai/user/0x-professor)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to produce repeatable transformer fine-tuning run plans, including task settings, training hyperparameters, evaluation cadence, and model-card scaffolding for Hugging Face or PyTorch workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review reports under-disclosed local file-write behavior in the helper script.

Mitigation: Use explicit, non-sensitive output paths and review generated files before relying on them.

Risk: The security review notes that --dry-run should not be relied on to avoid filesystem changes until fixed.

Mitigation: Run the helper only in a controlled workspace and verify file changes after execution.

Risk: The security review identifies CSV handling risk when inputs may come from untrusted sources.

Mitigation: Prefer JSON or Markdown output for untrusted inputs and review CSV output before opening it in spreadsheet tools.

## Reference(s):

- [Finetune Guide](references/finetune-guide.md)
- [ClawHub Skill Page](https://clawhub.ai/0x-professor/skills/dl-transformer-finetune)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance, Files]

**Output Format:** [JSON, Markdown, or CSV fine-tuning plan files with human-facing guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can generate deterministic plan artifacts and model-card skeleton content from optional JSON input.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
