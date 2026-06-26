## Description: <br>
Helps users discover and install agent skills when they ask questions like "how do I do X", "find a skill for X", "is there a skill that can...", or express interest in extending capabilities. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jherculesqz](https://clawhub.ai/user/jherculesqz) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to find installable skills for specialized tasks, compare options, and produce install commands when they choose to add a skill. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may propose installing third-party skills or running package-manager commands. <br>
Mitigation: Review the package source, publisher reputation, and exact command before installing; avoid global no-confirm installs unless the source is trusted. <br>
Risk: Search results alone may not be enough to judge whether a skill is trustworthy or appropriate. <br>
Mitigation: Verify install counts, source reputation, and repository quality before recommending or installing a skill. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jherculesqz/find-skills-gitcode) <br>
- [Skills directory](https://skills.sh/) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, markdown] <br>
**Output Format:** [Markdown with inline bash commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include skill recommendations, install commands, and links for user review.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
