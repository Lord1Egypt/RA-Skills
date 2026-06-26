## Description: <br>
Builds and configures an AI software development team inside OpenClaw, including agent setup, project folder structure, coordination workflow, and model handoffs for mockup-driven UI work. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[encryptshawn](https://clawhub.ai/user/encryptshawn) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to set up a coordinated OpenClaw software development team with PM, engineering, development, QA, Asana, GitHub, queue files, and project-state conventions. It is intended for configuring team workflow and workspace files, not for directly handling credential values. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill coordinates setup through high-impact administrator, Asana, Git, and email dependency skills. <br>
Mitigation: Review the delegated skills before use and use recovery snapshots before and after setup. <br>
Risk: The setup requires sensitive credential access through dependency skills. <br>
Mitigation: Store real tokens in a secret manager and provide only environment variable names during setup. <br>


## Reference(s): <br>
- [Project Files Reference](references/project-files.md) <br>
- [Workflow Reference](references/workflow.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/encryptshawn/build-dev-team) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with structured setup steps and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces setup instructions and workspace file content for OpenClaw agents; does not read or store credential values.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
