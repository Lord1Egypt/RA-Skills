## Description:

Adaptive Socratic Questioning helps agents generate adaptive follow-up questions, reasoning paths, misconception flags, and teacher guidance to deepen student reasoning.

This skill is ready for commercial/non-commercial use.

## Publisher:

[perpetualhui](https://clawhub.ai/user/perpetualhui)

### License/Terms of Use:

MIT-0

## Use Case:

Educators, researchers, and academic mentors use this skill to guide learners through research design, data analysis, paper writing, critical thinking, and problem solving with structured Socratic questioning.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad trigger wording may steer academic or problem-solving requests into a Socratic questioning style when the user expects a direct answer.

Mitigation: Use the skill when guided reasoning is desired, and narrow trigger wording or prompt framing for contexts that require direct answers.

Risk: Questions may be less effective or culturally mismatched without teacher review and domain context.

Mitigation: Have educators review generated question chains for level, subject accuracy, and appropriateness before using them with learners.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/perpetualhui/skills/adaptive-socratic-questioning)
- [Publisher profile](https://clawhub.ai/user/perpetualhui)
- [Project homepage from ClawHub metadata](https://github.com/perpetualhui/adaptive-socratic-questioning)
- [README](README.md)
- [Evaluation definitions](evals/evals.json)
- [Test report](tests/test-report.md)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [JSON-style structured guidance with follow-up questions, reasoning paths, misconception flags, and teacher guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Questions are adapted to learner level, topic, and response depth.]

## Skill Version(s):

1.1.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
