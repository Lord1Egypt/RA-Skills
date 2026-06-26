## Description: <br>
Helps users discover and install agent skills when they ask questions like "how do I do X", "find a skill for X", "is there a skill that can...", or express interest in extending capabilities. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Dawnwangzi](https://clawhub.ai/user/Dawnwangzi) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent users use this skill to search for installable skills that match a requested task, compare options, and optionally install a selected skill. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill encourages broad triggering for skill discovery and could suggest installing third-party skills when the user did not intend to change their environment. <br>
Mitigation: Use it only after explicit user intent to search for skills, and confirm the selected source before installation. <br>
Risk: The example global auto-confirmed install command can persistently modify the user's skill environment. <br>
Mitigation: Do not run global auto-confirmed installs until the user approves, the source has been reviewed, and the installation impact is understood. <br>


## Reference(s): <br>
- [Skills CLI catalog](https://skills.sh/) <br>
- [Example skill listing](https://skills.sh/vercel-labs/agent-skills/vercel-react-best-practices) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose skill search and install commands; review installation commands before running them.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
