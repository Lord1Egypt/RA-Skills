## Description:

Provides AI and machine learning techniques for CTF challenges, including model analysis, adversarial examples, model extraction, prompt injection, membership inference, training data poisoning, fine-tuning manipulation, neural network analysis, LoRA adapter exploitation, and LLM jailbreaking.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gandli](https://clawhub.ai/user/gandli)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and security practitioners use this skill in authorized CTF or lab settings to identify applicable AI/ML attack techniques, inspect challenge artifacts, and draft commands or code for model and LLM challenge workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill includes directly runnable offensive prompt-injection, jailbreak, filter-evasion, file-access, SSRF, unsafe model-loading, adversarial ML, and model extraction workflows.

Mitigation: Use only in authorized, disposable CTF or lab environments with no real secrets, no cloud credentials, constrained filesystem access, restricted network egress, and human review before running commands.

Risk: Untrusted model files and broad package installation commands can expose the agent host to unsafe deserialization, supply-chain, or environment-contamination risks.

Mitigation: Avoid loading untrusted .pt files on a normal agent host, and pin or install dependencies inside an isolated virtual environment or container.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/gandli/skills/ctf-ai-ml)
- [SKILL.md](artifact/SKILL.md)
- [CTF AI/ML - Model Attacks](artifact/model-attacks.md)
- [CTF AI/ML - Adversarial ML](artifact/adversarial-ml.md)
- [CTF AI/ML - LLM Attacks](artifact/llm-attacks.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and Python code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose offensive AI/ML testing workflows that require human authorization, isolation, and review before execution.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
