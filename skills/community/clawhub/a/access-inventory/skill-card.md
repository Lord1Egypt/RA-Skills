## Description: <br>
Stop your AI agent from claiming it lacks access. One rule + one inventory table = no more hedging. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[joeytbuilds](https://clawhub.ai/user/joeytbuilds) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to create AGENTS.md guidance and an access inventory so agents can identify configured tools, services, and credentials before claiming access is unavailable. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security scan says the skill tells agents to persistently find and use local credentials before asking the user. <br>
Mitigation: Require explicit user approval before reading credential files, scanning environment variables, using authenticated services, or verifying credentials; record only non-secret service names, scopes, and status notes. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/joeytbuilds/access-inventory) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with tables and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces instructions for maintaining an access inventory; it does not execute commands itself.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
