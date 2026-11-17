## Description:

Build, update and honestly evaluate text classifiers with the open-source adaptive-classifier library, which learns new examples and new classes without retraining from scratch. Use for small labeled sets, label sets that change over time, and routing, intent or moderation tasks; not for large static datasets where standard fine-tuning is better.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sandeep85das](https://clawhub.ai/user/sandeep85das)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to build and incrementally update local text classifiers for small labeled datasets and changing labels, then evaluate their performance with held-out data and class-level metrics.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Creating or loading classifiers may download model files or datasets, and saved classifiers may contain sensitive labeled data.

Mitigation: Ask for approval before downloads; protect labeled data and saved classifier files.

Risk: Classifier predictions may be inaccurate or shift as examples and classes are added, especially for consequential moderation or routing decisions.

Mitigation: Evaluate with held-out data and per-class metrics after updates, check order sensitivity, and retain human review for consequential decisions.

Risk: The library version or model configuration may differ from the assumptions in the skill.

Mitigation: Check the installed library version and API compatibility before relying on the examples.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/sandeep85das/skills/adaptive-classifier)
- [adaptive-classifier project repository](https://github.com/codelion/adaptive-classifier)
- [Minimal example: intent routing with held-out evaluation](references/minimal_example.md)

## Skill Output:

**Output Type(s):** [Code, Shell commands, Guidance]

**Output Format:** [Markdown with Python code and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes evaluation guidance and local classifier save/load examples; model downloads require user approval.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
