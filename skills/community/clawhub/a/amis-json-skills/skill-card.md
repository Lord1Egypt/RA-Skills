## Description: <br>
Generates Baidu AMIS JSON Schema configurations for enterprise admin pages, including CRUD views, forms, dialogs, event actions, validation guidance, and responsive layouts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lumacoder](https://clawhub.ai/user/lumacoder) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to produce AMIS JSON for common admin workflows such as login, CRUD lists, search forms, detail and edit dialogs, selectable tables, wizards, and dashboards. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may be auto-loaded for generic UI requests where AMIS is not the intended framework. <br>
Mitigation: Explicitly select this skill only for AMIS UI generation and avoid it for non-AMIS interfaces. <br>
Risk: Generated templates include placeholder login, create, update, delete, and data-loading API actions. <br>
Mitigation: Review generated endpoints, authentication behavior, destructive actions, and backend authorization before deploying the JSON configuration. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/lumacoder/amis-json-skills) <br>
- [AMIS official documentation](https://baidu.github.io/amis/zh-CN/docs/index) <br>
- [AMIS GitHub repository](https://github.com/baidu/amis) <br>
- [AMIS Editor online demo](https://aisuda.github.io/amis-editor-demo/) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with JSON snippets, JavaScript validation helpers, and reusable AMIS template files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes preset templates with placeholder API endpoints and validation suggestions for generated AMIS schemas.] <br>

## Skill Version(s): <br>
1.0.1 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
