## Description: <br>
Convert Figma design files to pixel-level mobile-first static HTML/CSS pages with MCP-first extraction, REST fallback, layered DOM reconstruction, and visual diff validation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[elsemk](https://clawhub.ai/user/elsemk) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to turn Figma links, screenshots, or asset bundles into native static HTML and CSS while preserving mobile-first layout, real DOM structure, and visual fidelity. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow may use Figma credentials and optionally the local Claude credential store for Figma MCP. <br>
Mitigation: Prefer explicit FIGMA_MCP_TOKEN or FIGMA_TOKEN, review Claude CLI and MCP setup commands before running them, and do not share or commit callback URLs, code#state values, auth-lock files, or credential files. <br>
Risk: Generated static pages can diverge from the source design if extraction, assets, or responsive layout assumptions are incomplete. <br>
Mitigation: Use the skill's visual diff pipeline, mobile no-horizontal-scroll checks, real DOM reconstruction rules, and user confirmation criteria before treating the page as complete. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/elsemk/figma-to-static) <br>
- [Figma MCP Usage Reference](references/figma-mcp-usage.md) <br>
- [CSS Extraction Rules](references/css-extraction-rules.md) <br>
- [Standard Project Directory Structure](references/file-structure.md) <br>
- [Figma MCP Auth State Machine](references/mcp-auth-state-machine.md) <br>
- [Anti-Patterns](references/anti-patterns.md) <br>


## Skill Output: <br>
**Output Type(s):** [Code, Files, Shell commands, Configuration instructions, Guidance, Markdown] <br>
**Output Format:** [Markdown guidance with shell commands and generated static HTML/CSS file structure] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces native HTML/CSS assets and visual diff outputs when the workflow is executed.] <br>

## Skill Version(s): <br>
2.0.6 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
