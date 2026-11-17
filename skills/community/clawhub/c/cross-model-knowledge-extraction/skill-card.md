## Description:

Extracts structured capability signatures from skill documentation, including workflow steps, triggers, known limits, scripts, and decision rules for downstream model distillation and verification.

This skill is ready for commercial/non-commercial use.

## Publisher:

[qq435912743](https://clawhub.ai/user/qq435912743)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to turn teacher skill documentation into machine-readable JSON capability profiles before model distillation, signature synthesis, and adversarial verification.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The bundled learner can persist usage history, errors, notes, and preferences in learned_patterns.json.

Mitigation: Avoid recording secrets, confidential project details, or untrusted instruction-like text in learner notes or preferences; review the file before sharing or committing the skill.

Risk: The skill includes self-evolution guidance that encourages future behavior changes based on accumulated local history.

Mitigation: Review proposed behavior changes and scan the skill before deployment, especially after learner state or skill instructions change.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/qq435912743/skills/cross-model-knowledge-extraction)
- [Skill documentation](artifact/SKILL.md)
- [Signature extraction script](artifact/scripts/extract_signature.py)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Guidance]

**Output Format:** [JSON capability signature with optional Markdown guidance and bash commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Runs locally with Python standard library; includes a self-test mode.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
