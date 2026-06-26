## Description: <br>
Guides developers through publishing ClawHub skills, including metadata, environment-variable declarations, license-term acceptance, and post-publish checks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tudoubudou](https://clawhub.ai/user/tudoubudou) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and maintainers use this skill for guidance when preparing, publishing, updating, and validating ClawHub skill releases. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Publishing examples include commands that read a local ClawHub token or submit files. <br>
Mitigation: Review commands and file paths before allowing an agent to run them. <br>
Risk: Generic triggers such as publish or update may activate the skill unintentionally. <br>
Mitigation: Narrow triggers before release if accidental activation would disrupt the user's workflow. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/tudoubudou/clawhub-skill-publishing-guide) <br>
- [ClawHub skill publish API](https://clawhub.ai/api/v1/skills) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration] <br>
**Output Format:** [Markdown with inline bash, YAML, and Python examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes publishing checklists, command examples, and FAQ-style troubleshooting.] <br>

## Skill Version(s): <br>
1.2.1 (source: server release metadata; artifact frontmatter says 1.2.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
