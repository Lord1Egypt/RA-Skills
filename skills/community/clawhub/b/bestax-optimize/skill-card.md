## Description:

Helps developers reduce the built CSS size of apps using @allxsmith/bestax-bulma by measuring raw and compressed size and choosing a suitable stylesheet or modular Sass build.

This skill is ready for commercial/non-commercial use.

## Publisher:

[allxsmith](https://clawhub.ai/user/allxsmith)

### License/Terms of Use:

MIT-0

## Use Case:

Frontend developers use this skill to assess CSS transfer size and optimize Bestax/Bulma styles through a lighter shipped flavor, a selective Sass build, or unused import and icon-asset removal.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Removing helper styles or changing theme flavors can silently change an app's appearance.

Mitigation: Check component helper props, utility classes, and theme usage before switching flavors; rebuild and review affected pages.

Risk: Removing imports, icon assets, or dependencies may break features used indirectly.

Mitigation: Review proposed removals against app usage before applying them and verify the resulting build.

## Reference(s):

- [Bestax: Optimize CSS release](https://clawhub.ai/allxsmith/skills/bestax-optimize)
- [Modular Sass build reference](references/modular-build.md)
- [Optimizing CSS Size](https://bestax.io/docs/guides/getting-started/optimizing-css)
- [Modular Sass guide](https://bestax.io/docs/guides/getting-started/modular#option-c--hand-rolled-modular-scss-advanced)
- [CSS variations](https://bestax.io/docs/guides/getting-started/variations#file-size-comparison)

## Skill Output:

**Output Type(s):** [Analysis, Guidance, Code, Shell commands, Configuration]

**Output Format:** [Markdown with Sass and shell code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports measured raw and gzip CSS sizes before and after changes when build results are available.]

## Skill Version(s):

1.0.0 (source: server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
