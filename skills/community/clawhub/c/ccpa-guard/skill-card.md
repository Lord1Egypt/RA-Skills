## Description:

CCPA Guardrail is a local runtime privacy guard that scans AI application input and output for CCPA/CPRA personal information and can detect, mask, or block risky text.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wwumit](https://clawhub.ai/user/wwumit)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent builders use this skill to check user prompts or model outputs for California privacy-related personal information before sending text to an AI model, logs, or end users. It supports detect, mask, and block workflows for runtime privacy guardrails.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The guard is a local masking aid, not legal advice or proof of CCPA/CPRA compliance.

Mitigation: Use it as one control in a broader privacy program and have compliance decisions reviewed by qualified legal or privacy professionals.

Risk: Rule-based detection may miss unusual personal information formats or flag benign text.

Mitigation: Test on representative traffic, review findings during rollout, and tune handling policies before using block mode in high-impact workflows.

Risk: The security guidance notes a Chinese-language CLI/documentation set and a PRC-governed disclaimer.

Mitigation: Review the documentation and governing-law disclaimer before deployment so operators understand support, legal, and review expectations.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wwumit/skills/ccpa-guard)

## Skill Output:

**Output Type(s):** [text, json, shell commands, guidance]

**Output Format:** [Plain text or JSON CLI results; guidance may include command examples.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Local processing; JSON findings include categories, severities, positions, masked previews, decisions, and masked or blocked output.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
