## Description: <br>
Build secure access control with RBAC, ABAC, permissions, policies, and scope-based authorization. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ivangdavila](https://clawhub.ai/user/ivangdavila) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill to design authorization models, permission naming schemes, policy evaluation flows, and framework middleware for application access control. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated authorization code or policy designs may contain incorrect permission logic, overly broad scopes, or incomplete audit behavior. <br>
Mitigation: Review policy logic, permission scopes, audit logging, and cache invalidation before production use. <br>
Risk: Permission caches can allow stale grants after role, team, or sharing changes. <br>
Mitigation: Use short-lived or invalidatable caches and invalidate permissions when role assignments, team membership, or resource sharing changes. <br>
Risk: Frontend-only authorization checks can expose protected resources. <br>
Mitigation: Enforce authorization on the server and at resource-fetch boundaries, not only in routes or user interfaces. <br>


## Reference(s): <br>
- [Authorization skill page](https://clawhub.ai/ivangdavila/authorization) <br>
- [Authorization homepage](https://clawic.com/skills/authorization) <br>
- [Access Control Models](models.md) <br>
- [Implementation Patterns](patterns.md) <br>
- [Framework Middleware](middleware.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Configuration instructions] <br>
**Output Format:** [Markdown guidance with example code snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Documentation-only; no executable code or hidden access behavior.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
