## Description:

Helps developers implement and review frontend route guards, role-based permissions, login redirects, and session handling across common web frameworks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bovinphang](https://clawhub.ai/user/bovinphang)

### License/Terms of Use:

MIT

## Use Case:

Frontend developers use this skill to build and review protected routes, permission checks, and safe redirects in React Router, Next.js, Vue Router, and Nuxt applications.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Client-side route guards may be mistaken for complete authorization.

Mitigation: Enforce authorization on APIs, server components, loaders, and server actions as well.

Risk: Untrusted post-login redirect destinations can send users to unintended sites.

Mitigation: Allow only same-origin, permitted paths when processing login redirects.

## Reference(s):

- [Route Protection release on ClawHub](https://clawhub.ai/bovinphang/skills/fec-route-protection)
- [Project homepage (listed in release metadata)](https://github.com/bovinphang/frontend-craft)

## Skill Output:

**Output Type(s):** [Code, Guidance]

**Output Format:** [Markdown with code examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Examples cover loading, unauthenticated and unauthorized states, login redirects, and expired sessions.]

## Skill Version(s):

2.9.0 (source: release evidence, package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
