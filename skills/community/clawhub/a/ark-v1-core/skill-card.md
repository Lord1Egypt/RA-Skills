## Description:

ARK V1.1 (Declarative) is a universal constitutional layer that loads ARK.yaml to guide an agent's epistemic discipline.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mattlab69](https://clawhub.ai/user/mattlab69)

### License/Terms of Use:

CC-BY-SA-4.0

## Use Case:

Developers and agent operators use this skill to add a declarative constitutional prompt layer that emphasizes structure, integrity, truth, coherence, uncertainty marking, and scoped responses for important answers.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill applies a broad session-wide constitutional ruleset that may constrain, redirect, block, or reshape normal agent responses.

Mitigation: Install only when that behavior is intended, and review activation scope, rule precedence, and response-blocking behavior before deployment.

Risk: The skill may require confidence labels, uncertainty marking, validation prompts, and refusal or downgrade behavior for important answers.

Mitigation: Use it in workflows where those controls are acceptable, and verify that downstream users understand the declarative limits of the skill.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mattlab69/skills/ark-v1-core)
- [ARK README](artifact/readme.md)
- [ARK declarative ruleset](artifact/ARK.yaml)
- [ARK compliance badge](artifact/ARK_COMPLIANCE_BADGE.md)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Markdown or plain text agent responses guided by declarative configuration]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May require confidence labels, explicit uncertainty, refusal or downgrade behavior, and separation of operational and exploratory content for important answers.]

## Skill Version(s):

1.1.2 (source: ClawHub release metadata; artifact frontmatter states 1.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
