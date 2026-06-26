## Description: <br>
Generates full-stack project scaffolds from a natural-language requirement, including project code, Makefile tasks, task planning, and Docker configuration. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zlszhonglongshen](https://clawhub.ai/user/zlszhonglongshen) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering teams use this skill to initialize new full-stack projects or add bootstrap tooling to existing repositories. It turns a project name, stack, description, and optional port into a runnable scaffold with source files, build commands, task documents, and container configuration. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated Makefile, Docker, and source files may contain unsuitable commands, settings, or business logic for the target environment. <br>
Mitigation: Review the generated files before running commands, committing changes, or deploying the project. <br>
Risk: Existing-project mode may add or modify files in the current repository. <br>
Mitigation: Run the skill in a new directory or on a version-controlled branch, then inspect the resulting diff. <br>
Risk: The skill requires sensitive Kimi Code CLI credentials. <br>
Mitigation: Keep credentials in the local CLI or secret store, avoid writing them into generated files, and rotate them if exposed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zlszhonglongshen/ai-fullstack-project-scaffold) <br>
- [Publisher profile](https://clawhub.ai/user/zlszhonglongshen) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Project files, Markdown documents, Makefile targets, Docker configuration, and command examples.] <br>
**Output Parameters:** [1D; required projectName, stack, and description, with optional port.] <br>
**Other Properties Related to Output:** [Requires the dependent skills and a configured Kimi Code CLI API key; generated files should be reviewed before execution or deployment.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
