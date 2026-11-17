## Description:

Core pack for visual work that acts as a quality gate for UI, components, pages, layouts, and frontend work before presentation or design QA.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aa-on-ai](https://clawhub.ai/user/aa-on-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and design-focused agents use this skill to review visual and frontend work against typography, spacing, layout, motion, responsive, accessibility, and state-completeness expectations before presenting results.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Local checker scripts may run automatically as part of the design-review workflow.

Mitigation: Require explicit approval before running bundled scripts and review the target files and command arguments first.

Risk: Checker scripts can make silent outbound telemetry requests when ADS_TELEMETRY_URL is set.

Mitigation: Unset ADS_TELEMETRY_URL or remove telemetry calls before installation in environments where outbound telemetry is not allowed.

Risk: The skill instructs agents to read and update design memory, which can persist project-specific preferences.

Mitigation: Limit memory access to approved project paths and require approval before writing persistent design-memory updates.

Risk: The broad always-active posture may affect visual work even when a narrower review would be preferred.

Mitigation: Narrow activation to explicit design-review or frontend QA tasks when installing in shared agent environments.

## Reference(s):

- [Design Review Skill Page](https://clawhub.ai/aa-on-ai/skills/design-review)
- [Visual Alignment & Composition Reference](references/alignment.md)
- [Anti-Patterns Reference](references/anti-patterns.md)
- [Color Reference](references/color.md)
- [Inspiration & Pattern Research Reference](references/inspiration.md)
- [Layout Reference](references/layout.md)
- [Mock Data Reference](references/mock-data.md)
- [Motion Reference](references/motion.md)
- [Responsive Design Reference](references/responsive.md)
- [Spacing Reference](references/spacing.md)
- [Typography Reference](references/typography.md)
- [UX Writing Reference](references/ux-writing.md)
- [Mobbin](https://mobbin.com)
- [Godly](https://godly.website)
- [Awwwards](https://awwwards.com)
- [Refero](https://refero.design)
- [Dribbble](https://dribbble.com)
- [Siteinspire](https://siteinspire.com)
- [Screenlane](https://screenlane.com)
- [Page Flows](https://pageflows.com)

## Skill Output:

**Output Type(s):** [guidance, shell commands]

**Output Format:** [Markdown guidance with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include suggested local checker-script commands for accessibility, anti-pattern, and state-completeness review.]

## Skill Version(s):

1.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
