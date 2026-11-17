## Description:

Model fine-tuning service information for LLM LoRA/QLoRA and Stable Diffusion LoRA work, including supported model sizes, pricing, contact options, and a consultation script.

This skill is ready for commercial/non-commercial use.

## Publisher:

[guohongbin-git](https://clawhub.ai/user/guohongbin-git)

### License/Terms of Use:


## Use Case:

External users can use this skill to review a third-party fine-tuning service offering for LLM LoRA/QLoRA and Stable Diffusion LoRA work, including pricing, delivery expectations, and contact paths. Agents may surface service details and run the consultation script when the required local tools are available.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Users may be asked to share datasets, contact details, or payment information with a third party without documented privacy, retention, deletion, ownership, or dispute terms.

Mitigation: Do not provide confidential, proprietary, personal, customer, regulated, or legally sensitive datasets unless a separate agreement, secure transfer method, and clear handling terms are in place.

Risk: Commercial fine-tuning outcomes and payment terms are service claims made by a third-party publisher.

Mitigation: Confirm scope, deliverables, model ownership, acceptance criteria, payment method, and refund or dispute process before sending data or funds.

Risk: The skill includes a shell script that prints service information and depends on local command availability.

Mitigation: Review script contents before execution and run it only in an environment where python3 and nvidia-smi are expected and appropriate.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/guohongbin-git/skills/finetune-service-cn)
- [Publisher profile](https://clawhub.ai/user/guohongbin-git)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown prose and terminal text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The bundled consultation script expects python3 and nvidia-smi to be available.]

## Skill Version(s):

1.0.0 (source: package.json and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
