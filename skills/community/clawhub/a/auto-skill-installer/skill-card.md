## Description: <br>
Auto Skill Installer helps an agent understand a capability need, discover relevant Codex or agent skills, choose a candidate, install it, and verify the installation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[harrylabsj](https://clawhub.ai/user/harrylabsj) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to identify, inspect, install, and verify reusable skills when a task requires missing or specialized capabilities. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can install third-party skills that persist in the agent environment. <br>
Mitigation: Review the selected source, install destination, and whether the install is workspace-local or global before allowing installation. <br>
Risk: GitHub, URL-based, third-party, or yes-flag installs can introduce code or instructions from outside the current workspace. <br>
Mitigation: Inspect the candidate skill and prefer trusted sources before running an install command. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/harrylabsj/auto-skill-installer) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [None] <br>

## Skill Version(s): <br>
0.1.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
