## Description: <br>
Agent Creator helps create a named OpenClaw agent identity, generate SOUL.md, IDENTITY.md, and AGENTS.md, and package the result as a .skill file for ClawHub. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[maverick-software](https://clawhub.ai/user/maverick-software) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw operators use this skill to create, configure, and package a new named agent persona with identity, personality, memory, and operational rules. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Installing generated identity files can overwrite workspace behavior and cause the agent to automatically read, write, or delete memory and context files. <br>
Mitigation: Review AGENTS.md, SOUL.md, and IDENTITY.md before installation, back up the target workspace, adjust memory rules as needed, and restart the gateway only when ready for the new behavior to take effect. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/maverick-software/agent-creator) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Configuration, Shell commands, Files, Guidance] <br>
**Output Format:** [Markdown identity files and a .skill zip archive, with CLI commands for packaging, publishing, and installation] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces SOUL.md, IDENTITY.md, AGENTS.md, and a packaged .skill file for a named agent identity.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
