## Description:

Generates structured answer templates for Cambridge International A-Level Physics (9702) questions, including question type, given and required quantities, formulae or principles, answer steps, and checks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kevin0818-lxd](https://clawhub.ai/user/kevin0818-lxd)

### License/Terms of Use:

MIT-0

## Use Case:

External learners, tutors, and developers use this skill to turn CIE 9702 physics questions into structured revision or solution-planning templates for exam preparation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Optional data-building tools include scraper and dependency risks separate from normal local inference.

Mitigation: Install in an isolated environment, pin or review dependencies, and avoid running the scraper or full retraining pipeline against untrusted sources until filename validation and path-containment checks are fixed.

Risk: DeepSeek teacher mode sends question and mark-scheme content to an external API during SFT data generation.

Mitigation: Use teacher mode only for non-sensitive content that is allowed to leave the environment, and keep DeepSeek credentials scoped to retraining workflows.

Risk: Adversarial evaluation artifacts show reduced robustness under some numeric and context perturbations.

Mitigation: Use the generated templates as exam-preparation guidance and require human review for final calculations, formula selection, and physics reasoning.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/kevin0818-lxd/skills/alevel-physics-cie)
- [Project Homepage](https://github.com/kevin0818-lxd/alevel-physics-cie)
- [Support Issues](https://github.com/kevin0818-lxd/alevel-physics-cie/issues)
- [Answer Template Format](skill/references/answer_template_format.md)
- [Training Pipeline Reference](skill/references/training.md)
- [Adversarial Evaluation Report](data/eval/adversarial_report_v1.1.json)
- [Xie et al. 2024](https://arxiv.org/abs/2402.17916)
- [FRANK CIE Source Site](https://cie.fraft.org)

## Skill Output:

**Output Type(s):** [markdown, guidance]

**Output Format:** [Structured Markdown with plain-text equations and sections for question type, given, required, formulae/principles, answer frame, and checks.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Normal inference is local MLX generation; final equations should be shown as plain text without LaTeX delimiters.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
