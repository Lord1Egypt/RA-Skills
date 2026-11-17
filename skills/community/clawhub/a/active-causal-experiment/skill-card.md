## Description:

Active Causal Experiment helps an agent choose information-rich do-operation interventions, update Bayesian beliefs over competing causal structures, and identify the most likely causal graph with fewer experiments.

This skill is ready for commercial/non-commercial use.

## Publisher:

[qq435912743](https://clawhub.ai/user/qq435912743)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, analysts, and agent builders use this skill to rank interventions by expected information gain, run causal-structure identification demos or self-tests, and reason about A/B or other intervention experiments across competing causal hypotheses.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The bundled learner stores usage history, errors, notes, and preferences across sessions.

Mitigation: Review the skill before installing, keep sensitive data out of notes and preferences, and inspect learned_patterns.json before sharing or reusing the skill.

Risk: The learning workflow encourages future changes to the skill instructions based on accumulated patterns.

Mitigation: Manually review and scan any proposed instruction updates before copying learned_patterns.json content or learner recommendations into SKILL.md.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/qq435912743/skills/active-causal-experiment)

## Skill Output:

**Output Type(s):** [Guidance, Code, Shell commands, Configuration]

**Output Format:** [Markdown with inline Python and bash references]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces local deterministic Python workflow guidance and may update a local learned_patterns.json file when the bundled learner is invoked.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
