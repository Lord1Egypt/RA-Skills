## Description: <br>
Helps users discover and install agent skills when they ask questions like "how do I do X", "find a skill for X", "is there a skill that can...", or express interest in extending capabilities. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[leochan14](https://clawhub.ai/user/leochan14) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent users use this skill to search for relevant installable skills, present candidate skills with install commands and reference links, and help with installation when the user chooses to proceed. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can recommend installation of third-party skills, including global no-confirm installation when a user chooses to proceed. <br>
Mitigation: Review the exact package name, source page, publisher, and repository before installation; avoid global no-confirm installation unless the selected skill is trusted. <br>
Risk: Skill search results may be incomplete or may not match the user's intent. <br>
Mitigation: Present candidate skills with their names, install commands, and source links so the user can review relevance before installing. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/leochan14/find-skills-0-1-0) <br>
- [Skills Directory](https://skills.sh/) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and links] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include candidate skill names, install commands, source links, and direct guidance when no matching skill is found.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata; artifact _meta.json lists skill package version 0.1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
