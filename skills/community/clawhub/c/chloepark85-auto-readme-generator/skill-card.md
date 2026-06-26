## Description: <br>
Generates a professional README.md file for a project, including name, description, installation, usage, and license sections based on project contents. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chloepark85](https://clawhub.ai/user/chloepark85) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to create a starter README.md for a local project with standard description, installation, usage, and license sections. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The generator can overwrite an existing README.md in the target project path. <br>
Mitigation: Run it only against the intended path and back up or rename any existing README.md before generation. <br>
Risk: The generated README content is generic and may include license or usage text that does not match the project. <br>
Mitigation: Review and edit the generated README, especially the license and project-specific sections, before publishing or relying on it. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/chloepark85/chloepark85-auto-readme-generator) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, text, shell commands] <br>
**Output Format:** [README.md Markdown file plus a terminal status message] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes README.md to the requested project path and may replace an existing file.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
