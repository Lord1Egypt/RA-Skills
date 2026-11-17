## Description:

Detect, diagnose, and fix flaky tests by analyzing CI history, test timing, shared state, race conditions, and environment dependencies, then provide targeted fixes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[charlie-morrison](https://clawhub.ai/user/charlie-morrison)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and test engineers use this skill to find non-deterministic tests, classify likely causes such as timing, shared state, order dependence, network calls, or environment assumptions, and draft targeted fixes or quarantine plans.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The example multi-run shell workflow uses fixed /tmp paths that can collide with other users or stale files on shared systems.

Mitigation: Run the workflow in a private mktemp directory and avoid elevated privileges, as recommended by the security guidance.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, guidance]

**Output Format:** [Markdown reports with inline shell commands and code snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include proposed test fixes and quarantine recommendations.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
