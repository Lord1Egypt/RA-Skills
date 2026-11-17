## Description:

Guides frontend developers in designing server-state queries, caching, invalidation, mutations, optimistic updates, and data-loading boundaries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bovinphang](https://clawhub.ai/user/bovinphang)

### License/Terms of Use:

MIT-0

## Use Case:

Frontend developers use this skill to implement or review server-state fetching, cache keys, invalidation, pagination, SSR hydration, and mutation rollback without mixing server data with local UI state.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Incorrect mutation or optimistic-update code can leave application data inconsistent.

Mitigation: Review generated application code and test mutation failures, rollback, and cache invalidation before deployment.

## Reference(s):

- [Data Fetching on ClawHub](https://clawhub.ai/bovinphang/skills/fec-data-fetching)
- [Query patterns](artifact/references/query-patterns.md)

## Skill Output:

**Output Type(s):** [Guidance, Code]

**Output Format:** [Markdown with TypeScript examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Recommendations for loading, error, empty, and data states, cache invalidation, and rollback.]

## Skill Version(s):

2.9.0 (source: ClawHub release evidence and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
