## Description:

Create award-winning, memorable websites with advanced animations, creative interactions, and distinctive visual experiences for portfolios, agency showcases, product launches, and other projects where "wow factor" matters.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mkhaytman87](https://clawhub.ai/user/mkhaytman87)

### License/Terms of Use:

MIT

## Use Case:

Developers and designers use this skill to create memorable, high-craft websites with choreographed motion, distinctive typography, immersive scrolling, creative interactions, and 3D or WebGL effects when appropriate.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Copied CDN script references can create supply-chain exposure if used directly in a production site.

Mitigation: Self-host third-party scripts or add verified Subresource Integrity before production use.

Risk: Heavy animation, smooth scrolling, and custom cursors can harm accessibility or usability when applied without fallbacks.

Mitigation: Preserve reduced-motion support, keyboard navigation, adequate contrast, and treat custom cursors as optional effects.

Risk: Rich 3D, WebGL, and scroll animation effects can degrade page performance on lower-powered devices.

Mitigation: Optimize media, lazy-load below-fold content, prefer transform-based animation, and verify animation frame rate and Core Web Vitals.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mkhaytman87/skills/awwwards-design)
- [Code snippets](artifact/SNIPPETS.md)
- [Award-winning typography](artifact/TYPOGRAPHY.md)
- [Lenis CDN example](https://unpkg.com/lenis@1.1.18/dist/lenis.min.js)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline code blocks and implementation checklists]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include frontend code examples, animation patterns, typography recommendations, performance targets, and accessibility checks.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
