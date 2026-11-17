## Description:

Reviews BubbleTea TUI code for proper Elm architecture, model/update/view patterns, and Lipgloss styling.

This skill is ready for commercial/non-commercial use.

## Publisher:

[anderskev](https://clawhub.ai/user/anderskev)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to review Go BubbleTea terminal UI code for Elm architecture, model/update/view separation, component composition, and Lipgloss styling issues while avoiding common false positives.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill depends on an unbundled sibling review-verification-protocol skill, so final review behavior can vary if that dependency is missing or changed.

Mitigation: Review or bundle the referenced verification skill and confirm it is available at the expected sibling path before relying on the package.

Risk: Incorrect or unsupported review findings could lead developers to make unnecessary BubbleTea code changes.

Mitigation: Require concrete file and line evidence for major findings and apply the verification protocol before publishing review output.

## Reference(s):

- [Bubbles Component Reference](references/bubbles-components.md)
- [Component Composition](references/composition.md)
- [Understanding the Elm Architecture](references/elm-architecture.md)
- [Model & Update](references/model-update.md)
- [View & Styling](references/view-styling.md)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Guidance]

**Output Format:** [Markdown code review findings with file and line references]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Review findings are expected to be evidence-backed and checked against the referenced verification protocol.]

## Skill Version(s):

2.3.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
