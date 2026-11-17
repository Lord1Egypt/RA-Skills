# Agent implementation and mobile composition

Read this when a guideline steers agent-built interfaces, component registry adoption, or responsive art direction.

## Keep a concise execution contract

When an agent-facing contract is in scope, update the repository's existing design contract; create `DESIGN.md` only if no canonical equivalent exists. Record atmosphere, semantic roles, important component states, responsive behavior, motion, product-specific anti-patterns, and release checks. Link the canonical human-facing guideline for rationale instead of duplicating it. Do not create repository files for a documentation-only or audit-only request unless they are part of the requested output.

When useful, describe design variance, motion intensity, and visual density explicitly. Tie each choice to the product and viewport; do not import another skill's default settings without a reason.

## Compose mobile deliberately

For a responsive web product, normally keep one URL and content source while allowing different compositions. The guideline should not dictate an authentication or analytics architecture unless the task includes those systems.

Classify each section's narrow-view treatment:

- `preserve`: retain identity, important evidence, or an essential action
- `recompose`: retain content while changing hierarchy, order, or geometry
- `collapse`: expose secondary detail through an accessible disclosure
- `defer`: provide a clear path to supporting detail on another surface

Essential information and actions must remain available. Storyboard narrow layouts with real content instead of relying only on a stacked desktop grid. Use the supported widths and test long text, overflow, keyboard focus, target sizes, supported themes, and reduced motion. Distinguish the team's target-size policy from WCAG's minimum and its exceptions.

## Adopt registry components selectively

Registries such as 21st.dev supply implementation ideas, not design authority. Inspect authorship, exact license, dependencies, framework compatibility, keyboard behavior, semantic markup, focus, reduced motion, and token fit. Adapt the component to the product's semantic system before adoption.

## Review visual choices in context

Centered heroes, bento grids, pills, gradient text, glass, glow, and rounded containers may serve a product. Check whether each treatment helps its content or interaction rather than using or banning it by habit. Repeated effects and repeated card treatments are prompts to inspect hierarchy, not automatic defects. Use real copy and evidence in concepts so placeholder content does not hide layout failures.

## References and their purpose

- [VoltAgent Awesome Design MD](https://github.com/VoltAgent/awesome-design-md): examples of a readable visual contract for agents.
- [Taste Skill](https://github.com/Leonxlnx/taste-skill): explicit taste controls and preflight ideas; its defaults remain choices for its own workflow.
- [21st.dev](https://21st.dev/): discovery of component implementations; verify each item's adoption conditions.

Verify current sources when relying on them. Their inclusion does not grant permission to copy their code or assets.
