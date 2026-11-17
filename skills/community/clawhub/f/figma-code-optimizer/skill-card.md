## Description:

Generates production-oriented frontend code from selected Figma designs while reusing the project's component library and design tokens.

This skill is ready for commercial/non-commercial use.

## Publisher:

[garvin131](https://clawhub.ai/user/garvin131)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to turn a selected Figma frame or component into React-oriented frontend code that maps design elements to existing UI components and tokenized styles.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may guide an agent to use Figma MCP context, which can expose unintended design files or frames if access is broader than needed.

Mitigation: Limit Figma MCP access to the intended design file or frame and share only the context required for the requested code generation task.

Risk: Generated frontend code may contain incorrect component mappings, token choices, accessibility gaps, or form logic.

Mitigation: Review, test, and scan generated code before merging it into a project.

## Reference(s):

- [Component Library Reference](references/component-library.txt)
- [Design Tokens Reference](references/design-tokens.txt)
- [Sample Prompts](examples/sample-prompts.txt)

## Skill Output:

**Output Type(s):** [code, markdown, configuration, guidance]

**Output Format:** [Markdown with frontend code examples and implementation guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May rely on selected Figma context and project-specific component library and design token references.]

## Skill Version(s):

1.0.4 (source: server release metadata; artifact frontmatter lists 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
