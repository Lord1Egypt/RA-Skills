## Description:

Rewrite AI-drafted essays into more human-like academic prose using a fine-tuned MLX LoRA over Qwen3-8B, corpus-derived writing-pattern weights, and syntactic targets.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kevin0818-lxd](https://clawhub.ai/user/kevin0818-lxd)

### License/Terms of Use:

MIT-0

## Use Case:

Students, educators, and writing-tool developers use this skill to revise AI-drafted argumentative or academic essays into continuous prose with a more human academic style while preserving author stance and citations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Academic-integrity misuse or policy violations when rewriting essays for submission.

Mitigation: Use rewritten output only in ways allowed by the relevant institution, publisher, or course policy.

Risk: Local execution installs ML dependencies and downloads the base model on first use.

Mitigation: Install in a virtual environment and run only if comfortable with local ML dependencies and model downloads.

Risk: Sensitive essay content may be exposed if the optional hosted API is used remotely.

Mitigation: Use hosted API mode only on a controlled server with HTTPS, authentication, and logging practices that match the user's privacy requirements.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/kevin0818-lxd/skills/essay-humanizer)
- [Publisher profile](https://clawhub.ai/user/kevin0818-lxd)
- [24 AI writing patterns](references/patterns.md)
- [Training pipeline](references/training.md)
- [Hosted API](references/hosted_api.md)

## Skill Output:

**Output Type(s):** [text]

**Output Format:** [Plain text essay prose]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Preserves author stance and citations when present; avoids fabricated references and strips LaTeX dollar delimiters unless explicitly requested.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
