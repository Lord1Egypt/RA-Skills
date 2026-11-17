## Description:

Evaluates text decision systems against character- and word-level adversarial perturbations, scores robustness as 1 minus flip rate, and suggests normalization or denoising hardening steps.

This skill is ready for commercial/non-commercial use.

## Publisher:

[qq435912743](https://clawhub.ai/user/qq435912743)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill before launching or red-teaming text classifiers, moderation systems, or routing decisions to find inputs where small perturbations flip decisions. It can also guide basic input-normalization hardening after fragility is found.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Local learning history can retain free-form notes, errors, and preferences that may include sensitive information.

Mitigation: Avoid entering secrets, confidential prompts, customer data, or sensitive incident details in learner notes, errors, or preferences.

Risk: Persistent learned state can influence future skill behavior and recommendations without enough user control.

Mitigation: Review or delete learned_patterns.json before sharing, publishing, reusing, or relying on accumulated recommendations.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/qq435912743/skills/adversarial-robustness)

## Skill Output:

**Output Type(s):** [Analysis, Code, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown with inline bash commands and JSON robustness results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses local Python scripts and may update learned_patterns.json when the learner module is invoked.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
