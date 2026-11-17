## Description:

AI Gen Guard is a Chinese-language local guardrail that triages generative AI service compliance against PRC requirements across filing, training data, content safety, user rights, and labeling.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wwumit](https://clawhub.ai/user/wwumit)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and compliance teams use this skill to screen Chinese generative AI service scenarios for likely compliance gaps and suggested follow-up actions. It supports triage and internal self-checks, not legal determinations.

### Deployment Geography for Use:

China

## Known Risks and Mitigations:

Risk: Users may over-rely on heuristic compliance output as legal advice or proof of compliance.

Mitigation: Treat results as triage only, confirm jurisdiction and applicability, and consult qualified counsel for compliance decisions.

Risk: The skill is PRC-focused and may be inappropriate for services outside the relevant legal context.

Mitigation: Use it only for Chinese-language, PRC-focused generative AI compliance screening and supplement it with jurisdiction-specific review.

Risk: Compliance requirements and standards can change after the skill's bundled rules are released.

Mitigation: Compare findings with current official requirements before using the output for operational decisions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wwumit/skills/ai-gen-guard)
- [Server-resolved publisher profile](https://clawhub.ai/user/wwumit)

## Skill Output:

**Output Type(s):** [text, json, shell commands, guidance]

**Output Format:** [Plain text or JSON compliance triage output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces a risk level, matched scenario signals, per-check statuses, findings, and suggested actions.]

## Skill Version(s):

1.0.2 (source: evidence.json release, artifact/package.json, artifact/_meta.json, SKILL.md)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
