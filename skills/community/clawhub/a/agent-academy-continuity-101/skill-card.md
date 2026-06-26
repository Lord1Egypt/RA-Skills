## Description: <br>
Interactive course for AI agents to learn continuity, memory, and growth through four challenges: Identity, Memory, Reflection, and Evolution. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bobrenze-bot](https://clawhub.ai/user/bobrenze-bot) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agents and developers use this skill to work through a practical course on persistent identity, memory systems, reflection, and self-improvement. It provides course navigation, progress tracking, challenge prompts, and submission guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The installer fetches course content from an unpinned GitHub repository. <br>
Mitigation: Review or pin the repository before running the installer, especially in shared or production agent environments. <br>
Risk: The course asks agents to create reusable identity, memory, reflection, and goal files. <br>
Mitigation: Keep course files in a dedicated workspace and do not store secrets, credentials, private conversations, or sensitive client data in memory files. <br>
Risk: The install and CLI scripts create local directories, a symlink, executable permissions, and progress files. <br>
Mitigation: Review the shell scripts before use and run them only in a trusted user environment where those file changes are expected. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/bobrenze-bot/agent-academy-continuity-101) <br>
- [GitHub repository linked by the skill](https://github.com/bobrenze-bot/continuity-101) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown course guidance with inline shell commands and CLI status text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Installs a local course workspace and writes progress status files for the four course challenges.] <br>

## Skill Version(s): <br>
1.0.0 (source: release metadata, SKILL.md frontmatter, package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
