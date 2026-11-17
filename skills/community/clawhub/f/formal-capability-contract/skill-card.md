## Description:

Defines machine-checkable preconditions, postconditions, and invariants for agent capabilities and validates execution traces to report whether a capability run satisfies its formal contract.

This skill is ready for commercial/non-commercial use.

## Publisher:

[qq435912743](https://clawhub.ai/user/qq435912743)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to specify formal contracts for agent actions, functions, or planning steps and to check real execution traces for clause-level violations and a provable correctness score.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent learning can store user notes, preferences, and failure details locally.

Mitigation: Do not record secrets or sensitive personal data in learner notes or preferences, and review learned_patterns.json before sharing or publishing the skill.

Risk: Learned recommendations or self-modification guidance could change future skill behavior without sufficient review.

Mitigation: Require human review before applying learned content to future behavior or writing any changes into SKILL.md.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/qq435912743/skills/formal-capability-contract)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with bash command examples and JSON verification results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May record local usage outcomes and preferences when the bundled learner script is invoked.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
