## Description:

Guides agents to solve derivative problems about root existence, root counts, and parameter ranges by converting derivative and limit analysis into concrete point-selection, sign-change, continuity, and intermediate-value proofs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jiuxiao-yunwai](https://clawhub.ai/user/jiuxiao-yunwai)

### License/Terms of Use:

MIT-0

## Use Case:

External learners, educators, and developers use this skill to solve or rewrite high-school and college-entrance-exam style derivative problems into grader-friendly proofs. It is especially useful when an agent must justify root existence, root count, or parameter ranges with explicit selected points and sign-change arguments.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill is Chinese-focused and may not match every learner's language needs, curriculum, or examination style.

Mitigation: Review the generated explanation for language, notation, and curriculum fit before using it in instruction or assessment.

Risk: Educational math guidance can still produce an incorrect proof, omit an endpoint case, or choose points that do not establish the required sign change.

Mitigation: Check derivative signs, domains, endpoint cases, continuity intervals, and selected-point inequalities before relying on the final proof.

Risk: Installation guidance uses standard git clone commands into local skill folders.

Mitigation: Install only from a trusted publisher or repository and review the skill files before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jiuxiao-yunwai/skills/derivative-point-picking)
- [README](README.md)
- [Root existence and parameter range example](examples/01-root-existence-parameter-range.md)
- [Exponential positive point example](examples/02-exponential-positive-point.md)
- [Negative interval point example](examples/03-negative-interval-point.md)
- [Local bound derivative example](examples/04-local-bound-derivative.md)
- [Sequence explicit n example](examples/05-sequence-explicit-n.md)
- [Log transform three roots example](examples/06-log-transform-three-roots.md)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown proof guidance with mathematical notation]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Bilingual Chinese and English guidance; no code execution required.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
