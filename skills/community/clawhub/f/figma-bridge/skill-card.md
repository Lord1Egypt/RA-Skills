## Description:

Extract design information from Figma files, including design tokens, component structure, colors, typography, spacing, and exportable assets for development workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[vanthienha199](https://clawhub.ai/user/vanthienha199)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to inspect Figma designs, extract reusable design tokens, summarize components, export assets, and translate Figma styles into implementation-ready CSS, JSON, or Tailwind configuration.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires a Figma Personal Access Token for read-only API access.

Mitigation: Use a token with the minimum Figma access needed, provide it through FIGMA_TOKEN only for this task, and rotate or revoke it if it is no longer needed.

Risk: Exported design assets may be saved locally under ./figma-exports/.

Mitigation: Review the export directory after use and remove sensitive or unnecessary design files from the local workspace.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/vanthienha199/skills/figma-bridge)
- [Figma REST API endpoint pattern](https://api.figma.com/v1/[endpoint])
- [Figma design URL pattern](https://www.figma.com/design/[FILE_KEY])

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with CSS, JSON, JavaScript, and shell command code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce local asset export paths under ./figma-exports/ when the user requests asset export.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
