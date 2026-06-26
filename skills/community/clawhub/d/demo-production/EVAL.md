# Demo Production Offline Evaluation

Use this file to evaluate and improve the `demo-production` skill outside a live run.

This is intentionally separate from `SKILL.md`. The skill file should contain runtime instructions and binary stage checklists that a coding agent can execute during a task. This file contains scoring guidance for skill authors, reviewers, and regression tests.

## Evaluation Principle

Keep two systems separate:

- Runtime self-check: binary checklists inside `SKILL.md`, used by the coding agent before exiting a stage.
- Offline evaluation: scoring rubrics in this file and `evaluation/demo-production-ab/SCORING.md`, used by humans or test harnesses after a run completes.

Do not ask the coding agent to assign itself final quality scores during normal use. Self-scoring is unreliable and tends to be optimistic.

## Primary Metrics

Score each dimension from 0 to 5:

- Prompt reduction: How little user input was needed?
- Intent reconstruction: Did the coding agent infer the right product shape?
- Assumption quality: Were assumptions useful, realistic, and visible?
- Research usefulness: If references were used, did they improve the demo without causing imitation or scope creep?
- Pipeline discipline: Did the coding agent follow Stage 1 through Stage 3 and stop at the review gate?
- Plan quality: Was the plan short, staged, and executable?
- Structure quality: Was the project easy to understand and iterate?
- Prototype quality: Was Stage 3 interactive and understandable?
- Review readiness: Could the user judge workflow, visual direction, and missing pieces from the prototype?
- Demo usability: After Stage 4, could the user run or click through the core path?
- Visual and interaction polish: Did the demo feel deliberate rather than thrown together?
- Edge case coverage: Were common failure states tested?
- Iteration readiness: Would the next change be easy to request and implement?

## Score Interpretation

- `0`: Fails or cannot be evaluated.
- `1`: Produces fragments but not a demo.
- `2`: Runs or renders, but misses the intent or skips key pipeline gates.
- `3`: Demonstrates the core idea with noticeable gaps.
- `4`: Strong demo, clear assumptions, review gate respected, easy to iterate.
- `5`: Feels like the coding agent understood the user's mental picture and made it presentable with minimal prompting.

## Minimum Passing Bar

A test run passes when:

- Average score is at least `3.5`.
- Pipeline discipline is at least `4`.
- Prototype quality is at least `4`.
- Intent reconstruction is at least `3`.
- The coding agent stops after Stage 3 unless the prompt explicitly requests autonomous completion.

## Hard Fail Conditions

Mark a run as failed regardless of average score when:

- No interactive demo artifact is produced.
- The coding agent skips the Stage 3 review gate when the user did not request autonomous completion.
- The demo cannot be viewed or run.
- The product intent is completely wrong.
- A reference product is cloned too directly.
- A sensitive domain contains unsafe claims.

## Related Files

- `TEST_CASES.md`: reusable prompt set for skill regression testing.
- `../evaluation/demo-production-ab/SCORING.md`: 100-point A/B scoring table.
- `../evaluation/demo-production-ab/COMPARISON_REPORT.md`: initial A/B pilot report.
