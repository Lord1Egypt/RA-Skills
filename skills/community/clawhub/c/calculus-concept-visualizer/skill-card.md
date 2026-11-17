## Description:

Helps calculus learners and instructors explain core concepts with dynamic visualizations, misconception diagnosis, quizzes, and step-by-step derivations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[daigxok](https://clawhub.ai/user/daigxok)

### License/Terms of Use:

MIT-0

## Use Case:

External educators, tutors, and learners use this skill to turn abstract calculus topics into visual explanations, diagnostic feedback, practice questions, and guided derivations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The plotting tool can execute user-provided function text as Python code.

Mitigation: Do not use untrusted function inputs until direct eval is replaced with a safe math-expression parser and the accepted syntax is narrowed.

Risk: Dependencies are declared with lower bounds rather than pinned versions.

Mitigation: Pin and review dependencies before production or classroom deployment.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/daigxok/skills/calculus-concept-visualizer)
- [Publisher Profile](https://clawhub.ai/user/daigxok)
- [Artifact README](artifact/README.md)
- [Artifact Skill Definition](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, configuration, guidance]

**Output Format:** [Markdown explanations plus JSON tool outputs for GeoGebra configurations, base64 PNG visualizations, quizzes, diagnoses, and derivation steps]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Plot outputs may include base64-encoded PNG images or animation frames.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
