## Description: <br>
Helps agents design, critique, polish, and harden frontend interfaces across websites, dashboards, app shells, components, forms, onboarding, theming, typography, accessibility, performance, and responsive behavior. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[liyafeichina](https://clawhub.ai/user/liyafeichina) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and design-focused agent users use this skill to improve production frontend UI: planning interface shape, reviewing UX quality, polishing visuals, hardening edge states, adapting responsive layouts, and applying targeted code changes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Live mode can access the local browser context, inspect selected page DOM, start a localhost server, inject scripts, and modify workspace files. <br>
Mitigation: Install only when this active frontend design workflow is intended; avoid live mode on sensitive authenticated pages and review generated config, injected script tags, PRODUCT.md/DESIGN.md changes, and cleanup markers after each session. <br>
Risk: Design proposals and automated edits can introduce incorrect or misleading UI guidance. <br>
Mitigation: Review proposed changes and generated diffs before deployment, then run the project's normal tests, accessibility checks, and security scans. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/liyafeichina/frontend-design-polish) <br>
- [Brand Register](reference/brand.md) <br>
- [Product Register](reference/product.md) <br>
- [Craft Workflow](reference/craft.md) <br>
- [Shape Workflow](reference/shape.md) <br>
- [Critique Workflow](reference/critique.md) <br>
- [Audit Workflow](reference/audit.md) <br>
- [Polish Workflow](reference/polish.md) <br>
- [Live Iteration Workflow](reference/live.md) <br>
- [Color and Contrast](reference/color-and-contrast.md) <br>
- [Responsive Design](reference/responsive-design.md) <br>
- [Typography](reference/typography.md) <br>
- [UX Writing](reference/ux-writing.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance with code snippets, shell commands, design plans, review findings, and file edits when the agent applies changes.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May run local Node scripts, start a localhost server, inject browser helper scripts, inspect selected page DOM, generate PRODUCT.md or DESIGN.md context, and modify workspace files when the invoked workflow requires it.] <br>

## Skill Version(s): <br>
3.0.6 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
