## Description: <br>
Provides React and Next.js guidelines from Vercel Engineering for reducing visual instability, layout shifts, flickering, hydration issues, font loading problems, and related performance regressions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wu-uk](https://clawhub.ai/user/wu-uk) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents working on React or Next.js code use this skill to review performance, rendering, hydration, bundle, data-fetching, and caching practices before writing or refactoring UI code. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Examples involving session cookies or user activity logging could be applied in a way that records raw session identifiers. <br>
Mitigation: Avoid logging raw session cookies or tokens; redact, hash, or omit identifiers before adding logging code. <br>
Risk: Inline hydration scripts can create security or policy issues if agents interpolate untrusted values or ignore Content Security Policy requirements. <br>
Mitigation: Keep inline hydration scripts static and minimal, avoid untrusted interpolation, and verify the implementation against the application's CSP. <br>
Risk: Cross-request caching examples could be adapted to cache user data without proper tenant boundaries, authorization checks, TTLs, or invalidation. <br>
Mitigation: Cache user data only with explicit authorization, tenant or user scoping, bounded TTLs, and clear invalidation rules. <br>


## Reference(s): <br>
- [React cache documentation](https://react.dev/reference/react/cache) <br>
- [React Compiler documentation](https://react.dev/learn/react-compiler) <br>
- [SWR documentation](https://swr.vercel.app) <br>
- [Next.js after documentation](https://nextjs.org/docs/app/api-reference/functions/after) <br>
- [better-all GitHub repository](https://github.com/shuding/better-all) <br>
- [node-lru-cache GitHub repository](https://github.com/isaacs/node-lru-cache) <br>
- [How we optimized package imports in Next.js](https://vercel.com/blog/how-we-optimized-package-imports-in-next-js) <br>
- [How we made the Vercel Dashboard twice as fast](https://vercel.com/blog/how-we-made-the-vercel-dashboard-twice-as-fast) <br>
- [Vercel Fluid Compute documentation](https://vercel.com/docs/fluid-compute) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code] <br>
**Output Format:** [Markdown guidance with TypeScript and TSX code examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Documentation-only skill; it provides review guidance and code patterns rather than executable commands.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
