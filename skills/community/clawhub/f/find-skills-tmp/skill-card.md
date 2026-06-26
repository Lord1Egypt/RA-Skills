## Description: <br>
Helps users discover and install agent skills when they ask questions like "how do I do X", "find a skill for X", "is there a skill that can...", or express interest in extending capabilities. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhichengsong](https://clawhub.ai/user/zhichengsong) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to identify relevant installable skills, search the open skills ecosystem, and present install options with package names and links. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad activation and global noninteractive install guidance could lead users toward persistent third-party skill installs without enough review. <br>
Mitigation: Require the agent to show the package source, publisher, and exact install command before installation, and prefer sandboxed or non-global installation where available. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zhichengsong/find-skills-tmp) <br>
- [Skills directory](https://skills.sh/) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands] <br>
**Output Format:** [Markdown with inline shell commands and external skill links] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include recommended skills, package identifiers, source links, and install commands.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
