## Description: <br>
Use when choosing, implementing, reviewing, or refactoring frontend state ownership across React, Vue, Next.js, Nuxt, URL state, server state, form state, browser persistence, or global stores. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bovinphang](https://clawhub.ai/user/bovinphang) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and engineers use this skill to decide where frontend state should live, select an appropriate store or framework pattern, and plan safe state-management refactors. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Incorrect state ownership can duplicate server data, overuse global stores, or cause derived state to drift from its source. <br>
Mitigation: Use the skill's ownership checklist before implementation and verify loading, error, empty, refresh, fallback, route, and permission-change behavior. <br>
Risk: Browser persistence patterns can accidentally retain sensitive data or stale client state. <br>
Mitigation: Persist only explicit non-sensitive fields with schema versions, expiration rules, migration handling, and sensitive-data exclusions. <br>
Risk: Server-rendered applications can leak user-specific state if singleton stores are shared across requests. <br>
Mitigation: Create request-scoped stores for user data and avoid reading browser-only APIs during server rendering. <br>


## Reference(s): <br>
- [State Management Patterns](references/state-patterns.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/bovinphang/fec-state-management) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code] <br>
**Output Format:** [Markdown with frontend code examples and review steps] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include state ownership inventories, tool-selection rationale, store/API boundaries, and verification steps.] <br>

## Skill Version(s): <br>
2.5.0 (source: README.md, metadata.json, package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
