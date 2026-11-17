## Description:

Convert Figma design files to pixel-level, mobile-first static HTML/CSS pages using Figma MCP extraction, REST fallback, layered DOM reconstruction, and visual diff validation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[elsemk](https://clawhub.ai/user/elsemk)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to turn Figma links, design screenshots, or asset bundles into static HTML/CSS pages while preserving mobile-first layout, real DOM structure, and visual fidelity. It is intended for static page restoration workflows, not React, Vue, SPA, server-rendered, or JavaScript-heavy applications.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can handle short-lived OAuth artifacts and optionally read Claude-stored Figma credentials.

Mitigation: Prefer explicit FIGMA_MCP_TOKEN or FIGMA_TOKEN values, avoid pasting live auth codes into logged shells, and use the provided state/session validation checks before submitting auth artifacts.

Risk: The setup path may modify user-level Claude/Figma MCP configuration or install global CLI tooling.

Mitigation: Review setup scripts before use and run the safe status/preflight path unless an interactive login flow is explicitly intended.

Risk: Preview hosting can expose local project contents if bound publicly or served from an overly broad directory.

Mitigation: Bind previews to 127.0.0.1 where possible, or serve only a sanitized and authenticated preview directory.

Risk: Generated static pages may diverge from the source design or accidentally simplify real DOM structure into images.

Mitigation: Use the visual diff pipeline, inspect region heatmaps, keep navigation and text as real DOM, and require human review before deployment.

## Reference(s):

- [Figma MCP Usage Reference](references/figma-mcp-usage.md)
- [CSS Extraction Rules](references/css-extraction-rules.md)
- [Reusable CSS Patterns](references/css-patterns.md)
- [Standard Project Directory Structure](references/file-structure.md)
- [Figma MCP Auth State Machine](references/mcp-auth-state-machine.md)
- [Anti-Patterns](references/anti-patterns.md)
- [ClawHub skill page](https://clawhub.ai/elsemk/skills/figma-to-static)
- [Publisher profile](https://clawhub.ai/user/elsemk)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and generated static HTML/CSS project files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce assets, CSS, HTML files, validation reports, and visual diff outputs when used by an agent.]

## Skill Version(s):

2.0.6 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
