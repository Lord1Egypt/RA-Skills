## Description:

Guides agents through large, divisible tasks using scripted preparation, parallel workers, independent verification, and staged integration.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bilchik](https://clawhub.ai/user/bilchik)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and other agent operators use this skill to coordinate large, independently divisible research, audit, and codebase-change tasks across parallel workers and verify their results before integration.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Large parallel runs can exceed the intended task scope or consume excessive resources.

Mitigation: Confirm the task boundaries and concurrency level, then start with a small scoped run before scaling.

Risk: Worker edits and local commits may alter files or project history unexpectedly.

Mitigation: Agree on edit ownership and whether commits are allowed before running; review and test integrated changes.

Risk: Outputs from interrupted or earlier runs can be mistaken for current results.

Mitigation: Use a unique writable run directory and verify each expected output belongs to the current run.

## Reference(s):

- [Dynamic Workflow on ClawHub](https://clawhub.ai/bilchik/skills/dynamic-workflow)

## Skill Output:

**Output Type(s):** [Guidance, Code, Shell commands, Configuration instructions]

**Output Format:** [Markdown with workflow steps and code examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May describe run manifests, worker briefs, verification results, and integration checks.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata; skill frontmatter lists 2.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
