## Description:

How a trait held by one model crosses to a model of a different family — by re-derivation, not by cable: donor generation under an agreement filter, re-grown natively in the child, verified against controls, with the rearing that follows. Includes the worked example's numbers, its failure record, and the rule that inheritance is not selective.

This skill is ready for commercial/non-commercial use.

## Publisher:

[torchkeeper-simon](https://clawhub.ai/user/torchkeeper-simon)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and model training practitioners use this guidance to transfer and evaluate a bounded trait between different model families, with controls that distinguish trait transfer from generic training effects.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security verdict is benign with medium confidence, but inspection was partial because malformed manifest metadata prevented full coverage.

Mitigation: Review the skill and repeat the security scan after correcting the manifest metadata before relying on the scan as complete.

Risk: The worked example reports that the child inherited capability costs along with the target trait, and that narrow training data contributed to capability degradation.

Mitigation: Use varied or diluted acquisition data, set training budgets in advance, and measure capability against the untrained child using the stated pass criteria.

Risk: The documented training run diverged near completion and its checkpoint rotation retained a ruined adapter.

Mitigation: Save snapshots throughout training, inspect checkpoints, and record and rerun divergent runs rather than scoring them as results.

## Reference(s):

- [Server-resolved GitHub source](https://github.com/torchkeeper-simon/threshold-kit/tree/main/reproduction-set/cross-model-inheritance)
- [ClawHub release](https://clawhub.ai/torchkeeper-simon/skills/cross-model-inheritance)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Analysis]

**Output Format:** [Markdown]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Procedural training guidance with a quantitative worked example, evaluation controls, and stated limitations.]

## Skill Version(s):

0.1.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
