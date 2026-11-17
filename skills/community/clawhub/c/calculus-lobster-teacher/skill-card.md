## Description:

Calculuslobt is a Chinese higher-mathematics teaching assistant for Tongji seventh-edition calculus topics, high-order learning tasks, exercise generation, and answer feedback.

This skill is ready for commercial/non-commercial use.

## Publisher:

[daigxok](https://clawhub.ai/user/daigxok)

### License/Terms of Use:

MIT-0

## Use Case:

External learners, instructors, and tutoring agents use this skill to explain Tongji seventh-edition higher-mathematics topics, design Bloom-aligned exercises, and provide structured feedback on calculus work.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Two sample exam reference files contain stray agent-control and tool-call text, which could confuse agents that load references as context.

Mitigation: Review before installing and remove the stray `</think>` and `StrReplace` blocks from both sample exam references before using the skill in agents that can edit files or follow loaded reference text.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/daigxok/skills/calculus-lobster-teacher)
- [Calculus topics reference](artifact/references/calculus-topics.md)
- [High-order comprehensive sample exam](artifact/references/sample-exam-v2.1.0.md)
- [Spatial analytic geometry sample exam](artifact/references/sample-exam-ch8-spatial-analytic-geometry.md)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown with structured explanations, exercise prompts, grading rubrics, and feedback notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Responses are educational guidance and should preserve textbook boundaries and uncertainty notes when page or theorem references need verification.]

## Skill Version(s):

2.1.1 (source: server release evidence and SKILL.md version table)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
