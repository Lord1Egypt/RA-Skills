## Description: <br>
Helps users discover and install agent skills when they ask questions like "how do I do X", "find a skill for X", "is there a skill that can...", or express interest in extending capabilities. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hanxueda](https://clawhub.ai/user/hanxueda) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to find installable skills for specialized tasks, present matching options, and offer installation commands when the user wants to extend agent capabilities. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A suggested global install could add a third-party skill the user did not intend to trust. <br>
Mitigation: Confirm the package name, source, and maintainer before installation, review the skill before deployment, and omit automatic confirmation flags when manual approval is preferred. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/hanxueda/find-skills-0) <br>
- [Skills directory](https://skills.sh/) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands] <br>
**Output Format:** [Markdown guidance with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose skill search and installation commands for user review.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
