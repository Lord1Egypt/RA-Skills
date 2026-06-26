## Description: <br>
Helps users discover and install agent skills when they ask questions like "how do I do X", "find a skill for X", "is there a skill that can...", or express interest in extending capabilities. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cs995279497-byte](https://clawhub.ai/user/cs995279497-byte) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to search for installable skills that match a requested task, compare candidate skills, and present install commands and reference links. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad user requests can lead to persistent third-party skill installation, including global installs that skip confirmation. <br>
Mitigation: Inspect the suggested skill source before installing, prefer explicit confirmation, avoid global silent installs unless the publisher is trusted, and confirm how to remove the skill afterward. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/cs995279497-byte/chen-find-skills) <br>
- [Skills directory](https://skills.sh/) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, markdown] <br>
**Output Format:** [Markdown with inline shell commands and links] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include install commands for third-party skills; review suggested skills before installation.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
