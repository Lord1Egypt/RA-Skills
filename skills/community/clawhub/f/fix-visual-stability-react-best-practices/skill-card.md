## Description:

React and Next.js guidance covering visual instability, layout shifts, CLS, flickering, hydration issues, font loading, and performance-oriented refactoring patterns.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wu-uk](https://clawhub.ai/user/wu-uk)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill when writing or refactoring React and Next.js code to reduce waterfalls, bundle size, layout shift, hydration flicker, avoidable re-renders, and common JavaScript performance costs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated code may expose session cookies, tokens, authorization headers, or other bearer credentials.

Mitigation: Review generated changes and require authentication and authorization data to remain server-side without logging raw credential material.

Risk: Inline pre-hydration scripts can create client-side security exposure if used for sensitive state.

Mitigation: Use inline pre-hydration scripts only for static, non-sensitive presentation state and pair them with an explicit CSP strategy.

Risk: An unpinned package execution command may run unexpected SVGO code.

Mitigation: Pin or locally install SVGO before using it in generated shell commands.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wu-uk/skills/fix-visual-stability-react-best-practices)
- [better-all](https://github.com/shuding/better-all)
- [How we optimized package imports in Next.js](https://vercel.com/blog/how-we-optimized-package-imports-in-next-js)
- [Rule sections](artifact/rules/_sections.md)

## Skill Output:

**Output Type(s):** [guidance, markdown, code, shell commands, configuration]

**Output Format:** [Markdown guidance with TypeScript and TSX examples plus occasional shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Documentation-only skill; output is advisory and should be reviewed before code changes are applied.]

## Skill Version(s):

0.1.0 (source: ClawHub release metadata; artifact metadata version is 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
