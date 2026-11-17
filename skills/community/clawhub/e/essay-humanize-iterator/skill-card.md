## Description:

Essay Humanize Iterator iteratively measures and revises essays to reduce AI-detection false positives while preserving meaning, citations, and natural writing style.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kevin0818-lxd](https://clawhub.ai/user/kevin0818-lxd)

### License/Terms of Use:

MIT-0

## Use Case:

Writers, educators, and writing-support agents use this skill to revise essays through a transparent measure-and-improve loop. It produces a polished essay plus an iteration report that shows AI-pattern, syntactic-complexity, and semantic-density metrics.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill is designed to make essays appear less AI-generated, which can be misused to conceal AI assistance or bypass academic or platform review.

Mitigation: Use it only for transparent editing and require users to follow applicable academic, workplace, and platform disclosure rules.

Risk: The security evidence flags shell-based measurement as under-scoped.

Mitigation: Run the skill in an isolated environment and pass essay text through files, stdin, or shell-free argument APIs rather than interpolating text into command strings.

Risk: The skill depends on spaCy and the en_core_web_sm model for measurement.

Mitigation: Pin the spaCy package and model version before deployment so scoring behavior is reproducible.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/kevin0818-lxd/skills/essay-humanize-iterator)
- [Publisher Profile](https://clawhub.ai/user/kevin0818-lxd)
- [Project Homepage](https://github.com/kevin0818-lxd/essay-humanize-iterator)
- [Issue Tracker](https://github.com/kevin0818-lxd/essay-humanize-iterator/issues)
- [Measurement Metrics](skill/references/metrics.md)
- [AI Writing Patterns](skill/references/patterns.md)
- [Iteration Strategy](skill/references/iteration_strategy.md)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Plain-text rewritten essay with a markdown iteration table and concise change summary]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill may also return structured JSON metrics when its measurement scripts are used directly.]

## Skill Version(s):

1.0.2 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
