## Description: <br>
Helps users discover and install agent skills when they ask questions like "how do I do X", "find a skill for X", "is there a skill that can...", or express interest in extending capabilities. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ruimin922](https://clawhub.ai/user/ruimin922) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to find installable skills for specialized tasks, compare relevant options, and optionally install a selected skill through the Skills CLI. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can suggest global installation of third-party skills while suppressing confirmation prompts. <br>
Mitigation: Require explicit user approval before running install commands, review the target skill source, publisher, permissions, and dependencies, and avoid `-g -y` unless persistent user-wide installation without prompts is intentional. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/ruimin922/find-skills-3) <br>
- [Skills catalog](https://skills.sh/) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include third-party skill links and install commands for user review.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
