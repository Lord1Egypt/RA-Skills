## Description:

Use when designing, reviewing, generating, or refactoring Feature-Sliced Design project structure for Effector ecosystem applications: layers, slices, segments, public APIs, imports, placement of Effector models, Farfetched operations, Atomic Router routes, Next.js adapters, and Steiger checks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[demark-pro](https://clawhub.ai/user/demark-pro)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to design, review, generate, and refactor Feature-Sliced Design structure for Effector ecosystem applications, including placement of Effector models, Farfetched operations, Atomic Router routes, Next.js adapters, public APIs, imports, and Steiger checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Optional Steiger setup snippets use npm/npx commands that can resolve mutable packages.

Mitigation: Pin exact package versions, commit a lockfile, and run the local pinned binary before using the tooling snippets.

Risk: Version-sensitive Effector, Farfetched, Atomic Router, and Next.js API details may change independently of this architecture guidance.

Mitigation: Verify exact API syntax against current official documentation before implementing generated code.

## Reference(s):

- [Effector FSD skill on ClawHub](https://clawhub.ai/demark-pro/skills/effector-fsd)
- [Feature-Sliced Design overview](https://feature-sliced.design/)
- [FSD layers reference](https://feature-sliced.design/docs/reference/layers)
- [FSD slices and segments reference](https://feature-sliced.design/docs/reference/slices-segments)
- [FSD public API reference](https://feature-sliced.design/docs/reference/public-api)
- [FSD Next.js guide](https://feature-sliced.design/docs/guides/tech/with-nextjs)
- [Effector documentation](https://effector.dev)
- [Farfetched documentation](https://ff.effector.dev)
- [Atomic Router protected route example](https://atomic-router.github.io/examples/protected-route.html)
- [Steiger](https://github.com/feature-sliced/steiger)
- [@effector/next](https://github.com/effector/next)
- [FSD core rules for Effector projects](references/01-core-rules.md)
- [Effector placement rules in FSD](references/02-effector-placement.md)
- [Farfetched placement in FSD](references/05-farfetched-placement.md)
- [FSD + Effector review checklist](references/07-review-checklist.md)
- [Effector audit ownership in FSD](references/11-effector-audit-ownership.md)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown with folder trees, TypeScript examples, shell commands, and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Documentation-only architecture guidance; optional tooling commands should be reviewed and pinned before execution.]

## Skill Version(s):

0.6.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
