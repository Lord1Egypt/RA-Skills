## Description:

Generate DESIGN.md files from any website URL by extracting visual design tokens such as colors, typography, spacing, components, and shadows into a structured markdown document for AI coding agents.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wavmson](https://clawhub.ai/user/wavmson)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and AI coding agents use this skill to document the visual language of a public or authorized website as a DESIGN.md file that can guide future UI generation. It is most useful when a team needs concrete colors, typography, spacing, component states, layout rules, and agent-ready prompts captured from a live site.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill opens arbitrary user-provided websites in an unsandboxed browser.

Mitigation: Run it only against public or explicitly authorized URLs from an isolated environment.

Risk: The evidence reports no restriction on internal URLs.

Mitigation: Avoid authenticated, private, localhost, and internal network pages unless the execution environment is deliberately isolated for that purpose.

Risk: The evidence notes missing overwrite protections for output paths.

Mitigation: Use a dedicated output directory and review generated files before moving them into a project.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/wavmson/skills/design-md-generator)
- [Google Stitch DESIGN.md Overview](https://stitch.withgoogle.com/docs/design-md/overview/)
- [Google Stitch DESIGN.md Format](https://stitch.withgoogle.com/docs/design-md/format/)
- [DESIGN.md Format Specification](references/format-spec.md)
- [Linear DESIGN.md Example](references/example-linear.md)
- [awesome-design-md](https://github.com/VoltAgent/awesome-design-md)

## Skill Output:

**Output Type(s):** [markdown, text, shell commands, code, guidance]

**Output Format:** [Markdown DESIGN.md with optional HTML previews and JSON design-token extraction output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses screenshots and extracted CSS tokens from a supplied URL; outputs should be reviewed before reuse.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
