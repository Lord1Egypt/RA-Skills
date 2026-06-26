## Description: <br>
Helps users discover and install agent skills when they ask questions like "how do I do X", "find a skill for X", "is there a skill that can...", or express interest in extending capabilities. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lvjunjie-byte](https://clawhub.ai/user/lvjunjie-byte) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to search for installable skills, compare relevant options, and receive installation guidance for extending an agent's capabilities. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may steer an agent toward broad third-party skill discovery or installation commands that skip confirmation. <br>
Mitigation: Review each suggested publisher and source link, prefer install commands without `-y`, and avoid global installs unless the user explicitly wants future sessions affected. <br>
Risk: Skill search results may be irrelevant, outdated, or unsuitable for the user's environment. <br>
Mitigation: Inspect the skill page and source before installation, and handle the task directly when no trustworthy matching skill is found. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/lvjunjie-byte/find-skills-lvjunjie) <br>
- [Skills ecosystem browser](https://skills.sh/) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands] <br>
**Output Format:** [Markdown with inline shell commands and links] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include suggested skill names, install commands, source links, and cautions about confirmation before installation.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
