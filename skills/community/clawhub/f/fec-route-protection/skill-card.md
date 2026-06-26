## Description: <br>
Route Protection guides agents implementing or reviewing frontend route guards, authentication state handling, redirects, RBAC, and permission checks across React Router, Next.js, Vue Router, and Nuxt. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bovinphang](https://clawhub.ai/user/bovinphang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and coding agents use this skill to design or review frontend route protection for private routes, role-based access, redirects, session expiry, and framework-specific route middleware. It is a reference guide and code-example source, not a replacement for backend authorization. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Frontend route protection can be mistaken for a complete security boundary. <br>
Mitigation: Enforce authorization again on APIs, SSR loaders, server actions, and backend routes, as stated in the server security guidance and artifact constraints. <br>
Risk: Example code may be copied without adapting redirect, tenant, role, or session-expiry handling to the application. <br>
Mitigation: Review and test direct private URL access, refresh behavior, role changes, redirect parameters, and tenant context before deployment. <br>


## Reference(s): <br>
- [ClawHub Route Protection page](https://clawhub.ai/bovinphang/fec-route-protection) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code] <br>
**Output Format:** [Markdown guidance with TypeScript, TSX, and framework-specific code examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Documentation-only output intended for adaptation and review; snippets must be paired with API, loader, server action, and backend route authorization.] <br>

## Skill Version(s): <br>
2.5.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
