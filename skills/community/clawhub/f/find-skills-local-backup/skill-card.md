## Description: <br>
Helps users discover and install agent skills when they ask questions like "how do I do X", "find a skill for X", "is there a skill that can...", or express interest in extending capabilities. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[12357851](https://clawhub.ai/user/12357851) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to search for installable skills that match a requested task, present relevant options, and provide Skills CLI commands for installing or updating skills. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Installing third-party skills globally while skipping prompts can add unreviewed behavior to future agent sessions. <br>
Mitigation: Review the skill source, publisher, and requested behavior before installation; prefer install commands without `-y` and avoid `-g` unless global availability is intended. <br>
Risk: Search results may point users to skills that are unsuitable, stale, or from publishers they do not trust. <br>
Mitigation: Present the publisher and source link with each recommendation and ask the user to confirm before installing a selected skill. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/12357851/find-skills-local-backup) <br>
- [Skills catalog](https://skills.sh/) <br>
- [Example Skills catalog entry](https://skills.sh/vercel-labs/agent-skills/vercel-react-best-practices) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown responses with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [None] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
