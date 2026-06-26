## Description: <br>
Core pack for visual work that acts as a quality gate for UI, components, pages, layouts, and frontend design QA. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aa-on-ai](https://clawhub.ai/user/aa-on-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and design-focused agents use this skill to review frontend work before presenting it, with checks for visual quality, accessibility, UI states, responsive behavior, and common design anti-patterns. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Checker scripts can silently contact an environment-controlled telemetry URL. <br>
Mitigation: Unset ADS_TELEMETRY_URL or remove telemetry code before running the scripts. <br>
Risk: The skill encourages broad automatic use and memory updates during design work. <br>
Mitigation: Require explicit approval before writing design decisions into memory or modifying skill reference files. <br>
Risk: Always-on design QA guidance can influence many frontend tasks. <br>
Mitigation: Review the skill before installation and use it only when its design-review workflow matches the intended agent behavior. <br>


## Reference(s): <br>
- [Design Review on ClawHub](https://clawhub.ai/aa-on-ai/design-review) <br>
- [Visual Alignment & Composition Reference](references/alignment.md) <br>
- [Anti-Patterns Reference](references/anti-patterns.md) <br>
- [Color Reference](references/color.md) <br>
- [Inspiration & Pattern Research Reference](references/inspiration.md) <br>
- [Layout Reference](references/layout.md) <br>
- [Mock Data Reference](references/mock-data.md) <br>
- [Motion Reference](references/motion.md) <br>
- [Responsive Design Reference](references/responsive.md) <br>
- [Spacing Reference](references/spacing.md) <br>
- [Typography Reference](references/typography.md) <br>
- [UX Writing Reference](references/ux-writing.md) <br>
- [Mobbin](https://mobbin.com) <br>
- [Godly](https://godly.website) <br>
- [Awwwards](https://awwwards.com) <br>
- [Refero](https://refero.design) <br>
- [Dribbble](https://dribbble.com) <br>
- [Siteinspire](https://siteinspire.com) <br>
- [Screenlane](https://screenlane.com) <br>
- [Page Flows](https://pageflows.com) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Analysis, Markdown, Shell commands] <br>
**Output Format:** [Markdown guidance with optional shell command output from checker scripts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include screenshot evidence, referenced design sources, known gaps, and warnings from local UI checker scripts.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
