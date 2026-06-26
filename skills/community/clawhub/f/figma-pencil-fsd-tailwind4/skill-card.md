## Description: <br>
Converts selected Figma or Pencil designs into production-ready frontend code using Feature-Sliced Design, Tailwind CSS v4, project tokens, and accessibility checks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[johnwayneeee](https://clawhub.ai/user/johnwayneeee) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and frontend engineers use this skill to translate scoped Figma or Pencil designs into code while preserving local architecture, design tokens, component reuse, accessibility, and validation expectations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated frontend changes may drift from the host repository's architecture, design tokens, component library, or accessibility expectations. <br>
Mitigation: Check local project contracts first, reuse existing primitives and tokens, review generated code and token changes, and run the project's type-check, lint, tests, and accessibility checks when available. <br>
Risk: The skill can guide an agent to edit frontend files and handle design assets when the user asks for implementation. <br>
Mitigation: Review source-control diffs, asset handling, and any generated commands before accepting changes. <br>
Risk: The Pencil workflow is documented as experimental compared with the Figma MCP workflow. <br>
Mitigation: Prefer Figma MCP when both design sources exist, or use Pencil only when the user explicitly requests it or it is the source of truth. <br>


## Reference(s): <br>
- [Project Contracts](references/project-contracts.md) <br>
- [FSD Mapping](references/fsd-mapping.md) <br>
- [Server / Client Boundaries](references/rsc-boundaries.md) <br>
- [Tailwind 4 Tokens](references/tailwind-tokens.md) <br>
- [Figma MCP Workflow](references/figma-mcp-workflow.md) <br>
- [Pencil Workflow](references/pencil-workflow.md) <br>
- [Accessibility Checklist](references/accessibility-checklist.md) <br>
- [Example: Frame to FSD](references/example-mapping.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/johnwayneeee/figma-pencil-fsd-tailwind4) <br>
- [ClawHub Publisher Profile](https://clawhub.ai/user/johnwayneeee) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with implementation plans, code edits, configuration snippets, and shell commands as needed.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs should be scoped to a selected frame, screen, or component and should include explicit validation status when checks cannot be run.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
