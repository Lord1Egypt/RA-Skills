## Description: <br>
Drafts FreeLattice form fields and, when the runtime supports artifacts, packages the resulting skill as a zip for import-style workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[neomagnetar](https://clawhub.ai/user/neomagnetar) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and FreeLattice creators use this skill to convert a plain-language skill idea into copy-ready FreeLattice form fields and a minimal import-style package. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated package files may include sensitive details if the user places secrets or account information in skill fields. <br>
Mitigation: Avoid entering secrets or sensitive account details, and review generated skill.json, README.md, and zip contents before import. <br>
Risk: Generated system prompts or package contents may contain unintended instructions for the target FreeLattice skill. <br>
Mitigation: Review the generated system prompt and package files before using the package in FreeLattice. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/neomagnetar/freelattice-skill-builder) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, configuration, files] <br>
**Output Format:** [Markdown sections with JSON package content and optional zip artifact] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can create a minimal skill.json, README.md, and zip package when the runtime supports file creation; otherwise emits manual package file contents.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
