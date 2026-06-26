## Description: <br>
Helps users discover and install agent skills when they ask questions like "how do I do X", "find a skill for X", "is there a skill that can...", or express interest in extending capabilities. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[baotangyin](https://clawhub.ai/user/baotangyin) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to search for installable skills, compare relevant options, and receive install commands or fallback guidance when no suitable skill is found. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The recommended global install command can install a skill for future sessions and skip the CLI confirmation prompt. <br>
Mitigation: Review the recommended skill source first, approve global installs intentionally, and remove `-y` when a confirmation prompt is preferred. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/baotangyin/find-skills-from-jimliuxinghai) <br>
- [Skills ecosystem browser](https://skills.sh/) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands] <br>
**Output Format:** [Markdown with inline bash code blocks and links] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include suggested skill names, links, install commands, and direct-help fallback guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
