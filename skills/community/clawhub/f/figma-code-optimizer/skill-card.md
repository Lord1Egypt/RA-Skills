## Description: <br>
Generates high-quality frontend code from Figma designs while reusing project components and design tokens. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[garvin131](https://clawhub.ai/user/garvin131) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers use this skill to turn selected Figma frames or components into React-oriented frontend code that maps to an existing component library, design tokens, responsive layout patterns, and accessibility expectations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Private code or design context may be exposed when review workflows send diffs or generated code to fallback reviewers. <br>
Mitigation: Review the selected Figma context and code diffs before using review automation on private projects. <br>
Risk: Generated frontend code may mis-map Figma layers, design tokens, or component props. <br>
Mitigation: Validate generated code against the project's component library, design-token reference, accessibility requirements, and responsive behavior before deployment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/garvin131/figma-code-optimizer) <br>
- [Component library reference](references/component-library.txt) <br>
- [Design tokens reference](references/design-tokens.txt) <br>
- [Sample prompts](examples/sample-prompts.txt) <br>


## Skill Output: <br>
**Output Type(s):** [Code, Markdown, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with frontend code snippets and component-mapping instructions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs are intended to be adapted to the user's connected Figma context, component library, and design-token definitions.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release metadata; artifact frontmatter says 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
