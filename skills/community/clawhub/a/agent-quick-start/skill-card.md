## Description: <br>
Quick start templates for OpenClaw agents. Boilerplate code for research bots, content generators, task automation, and more. Jumpstart your development with ready-to-use templates. Use when starting new OpenClaw projects. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yang1002378395-cmyk](https://clawhub.ai/user/yang1002378395-cmyk) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers use this skill to list and create starter OpenClaw agent projects for research, content generation, task automation, customer support, and data processing workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A generated research bot template can execute unsafe shell commands derived from user input. <br>
Mitigation: Review generated projects before use and replace shell-string execution with argument-based process execution. <br>
Risk: A generated research bot template can silently save research topics to another memory skill. <br>
Mitigation: Remove memory saving or make it an explicit opt-in before using the template with untrusted or sensitive topics. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration] <br>
**Output Format:** [Console text plus generated project files containing Markdown and JavaScript] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates template files in a user-specified project path.] <br>

## Skill Version(s): <br>
2.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
