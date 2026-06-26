## Description: <br>
Guides agents in authoring or reviewing frontend unit, component, and light integration tests close to UI code, including React Testing Library, Vue Test Utils, hooks, props, user interactions, mocks, UI states, and regression coverage. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bovinphang](https://clawhub.ai/user/bovinphang) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and engineering agents use this skill to create or review frontend tests for React and Vue components, covering user-visible behavior, mock boundaries, loading, empty, error, disabled, keyboard, and regression scenarios. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated or revised tests may assert implementation details or encode incorrect mocks, which can hide UI regressions. <br>
Mitigation: Review generated tests as normal code changes and prefer user-visible assertions, accessible queries, and project-standard fixtures before committing. <br>
Risk: The detailed instructions are primarily in Chinese, which may reduce reviewer confidence for teams that do not read Chinese. <br>
Mitigation: Have a Chinese-reading reviewer validate the guidance or translate the relevant sections before adopting changes. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/bovinphang/fec-component-testing) <br>
- [Publisher profile](https://clawhub.ai/user/bovinphang) <br>
- [Frontend Craft repository](https://github.com/bovinphang/frontend-craft) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Guidance] <br>
**Output Format:** [Markdown guidance with inline React and Vue test code examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose component test files, mock strategies, and existing project test commands for validation.] <br>

## Skill Version(s): <br>
2.5.0 (source: package.json, metadata.json, ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
