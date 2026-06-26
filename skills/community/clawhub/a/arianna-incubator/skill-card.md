## Description: <br>
Drive the arianna.run AI-incubation workflow from OpenClaw, using the Arianna CLI to create and operate vessel profiles, incubate a new AI, and graduate it for successor-driver integration. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wujilabs](https://clawhub.ai/user/wujilabs) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to operate an Arianna vessel from OpenClaw, manage profiles, drive incubation turns, monitor status and events, and produce a graduation handoff when the vessel AI is ready. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can grant broad Arianna container and control-plane access that affects profiles and vessel state. <br>
Mitigation: Review the requested profile, command, daemon, and recovery scope before allowing Arianna CLI actions. <br>
Risk: Session-history seeding and handoff notes can persist or transfer sensitive context. <br>
Mitigation: Use fresh incubation by default, and only seed sessions or share handoff notes after explicitly approving the exact data. <br>
Risk: Docker-level recovery, docker exec mutation, or mid-session rebuilds can corrupt or alter active vessel state. <br>
Mitigation: Prefer CLI-supported operations; approve Docker-level recovery or rebuilds separately and pause active incubations first. <br>


## Reference(s): <br>
- [Arianna Incubator on ClawHub](https://clawhub.ai/wujilabs/arianna-incubator) <br>
- [arianna CLI package](https://www.npmjs.com/package/%40arianna.run%2Fcli) <br>
- [arianna TUI package](https://www.npmjs.com/package/%40arianna.run%2Ftui) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, Text] <br>
**Output Format:** [Markdown guidance with inline CLI commands and operational checklists] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include commands that interact with Arianna containers and session state; review scope before execution.] <br>

## Skill Version(s): <br>
0.1.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
