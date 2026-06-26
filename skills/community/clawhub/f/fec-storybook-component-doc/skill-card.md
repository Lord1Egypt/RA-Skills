## Description: <br>
Guides agents in setting up and reviewing Storybook component documentation, design-system presentation, isolated component state previews, MDX docs, decorators, interaction checks, and visual baselines. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bovinphang](https://clawhub.ai/user/bovinphang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Frontend developers and design-system maintainers use this skill to create or review Storybook stories, decorators, MDX documentation, interaction tests, accessibility addons, and component-scoped visual baselines. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Storybook stories can drift from component props or design-system conventions and mislead consumers. <br>
Mitigation: Review generated stories and docs with component API changes, and keep variant, state, and token coverage synchronized with the implementation. <br>
Risk: Storybook visual baselines cover component states, not full cross-page user journeys. <br>
Mitigation: Use dedicated testing strategy or E2E workflows for route-level behavior, production-page screenshots, and broader coverage planning. <br>
Risk: Storybook and visual-regression commands may involve project tokens or generated static output. <br>
Mitigation: Keep project tokens in secret management and avoid committing generated Storybook build artifacts. <br>


## Reference(s): <br>
- [Storybook configuration and examples](references/story-patterns.md) <br>
- [ClawHub skill page](https://clawhub.ai/bovinphang/fec-storybook-component-doc) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with TypeScript, TSX, MDX, and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose Storybook configuration, stories, decorators, MDX documentation, interaction tests, accessibility checks, and visual baseline commands.] <br>

## Skill Version(s): <br>
2.6.0 (source: server release metadata, package.json, README, and metadata.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
