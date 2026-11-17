## Description:

Build UI components and pages using the AIOZ UI V3 design system, including token mapping, component imports, icons, typography, and chart guidance for React code.

This skill is ready for commercial/non-commercial use.

## Publisher:

[datnguyen26730](https://clawhub.ai/user/datnguyen26730)

### License/Terms of Use:


## Use Case:

Developers and agents use this skill to translate Figma MCP output into React UI code that follows AIOZ UI V3 component, token, typography, icon, and chart conventions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A chart reference filename mismatch may cause agents to look for references/charts.md even though the artifact provides references/chart.md.

Mitigation: Resolve or document the filename mismatch before relying on chart guidance; use the bundled references/chart.md file when validating chart behavior.

Risk: V2/V3 wording inconsistency in component guidance may cause agents to question which AIOZ UI conventions to use.

Mitigation: Confirm the intended AIOZ UI V3 package paths before deployment; use @aioz-ui/core-v3/components for non-chart UI and @aioz-ui/core/components for charts as stated in the current guidance.

## Reference(s):

- [AIOZ UI V3 Charts Reference](references/chart.md)
- [AIOZ UI V3 Color Token Reference](references/colors.md)
- [AIOZ UI V3 Component Reference](references/components.md)
- [AIOZ UI V3 Icons Reference](references/icons.md)
- [AIOZ UI V3 Setup Reference](references/setup.md)
- [AIOZ UI V3 Typography Reference](references/typography.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with TypeScript/TSX, JSON, CSS, and shell/configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs are guidance and code/configuration suggestions for the requesting agent.]

## Skill Version(s):

1.0.1 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
