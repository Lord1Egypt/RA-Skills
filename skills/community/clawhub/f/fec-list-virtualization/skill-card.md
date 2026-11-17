## Description:

Guides developers in optimizing large scrolling lists with windowing, row measurement, and stable loading behavior.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bovinphang](https://clawhub.ai/user/bovinphang)

### License/Terms of Use:

MIT

## Use Case:

Developers and engineers use this skill to assess scrolling bottlenecks and implement accessible, performant virtualized lists and grids within their existing frontend stack.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Virtualized items outside the viewport may be absent from browser search, SEO indexing, and print output.

Mitigation: Keep search- or SEO-critical content accessible outside the virtual window and test print or export paths.

Risk: Windowing and dynamic heights can disrupt keyboard navigation, screen reader context, or scrolling stability.

Mitigation: Test focus and screen reader behavior, measure row heights, and tune overscan and scroll anchoring.

## Reference(s):

- [List virtualization patterns](references/virtualization-patterns.md)
- [ClawHub skill release](https://clawhub.ai/bovinphang/skills/fec-list-virtualization)

## Skill Output:

**Output Type(s):** [Guidance, Code, Markdown]

**Output Format:** [Markdown with implementation guidance and code examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Framework-aware recommendations for list and grid virtualization.]

## Skill Version(s):

2.9.0 (source: ClawHub release, README.md, package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
