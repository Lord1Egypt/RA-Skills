## Description: <br>
FlowSwarm helps developers coordinate multi-agent coding swarms with RuFlo, Claude Code, MCP tooling, prompt templates, setup checks, and persistent memory for test generation, feature work, refactors, security audits, and quality loops. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[windseeker1111](https://clawhub.ai/user/windseeker1111) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering teams use this skill to plan and launch coordinated Claude Code swarm sessions for implementation, test generation, refactoring, security audit, and quality-loop tasks. It is intended for substantial coding work where multiple specialist roles, persistent memory, and MCP coordination can improve execution. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad persistent tooling and MCP auto-start can expand the actions available during agent runs. <br>
Mitigation: Install and run the skill only in trusted, version-controlled projects, and review `.mcp.json` before enabling autoStart. <br>
Risk: The artifact includes examples using permission bypass for Claude Code execution. <br>
Mitigation: Avoid `bypassPermissions` outside an isolated workspace and review generated changes before committing or deploying. <br>
Risk: Persistent swarm memory can retain sensitive or proprietary context supplied during coding sessions. <br>
Mitigation: Do not feed unsanitized secrets, logs, production data, or proprietary details into persistent memory. <br>
Risk: The setup flow uses `ruflo@latest`, which can change behavior between installations. <br>
Mitigation: Prefer pinned RuFlo versions when installing or registering MCP tooling. <br>


## Reference(s): <br>
- [FlowSwarm ClawHub Listing](https://clawhub.ai/windseeker1111/flow-swarm) <br>
- [Template Examples](references/template-examples.md) <br>
- [Setup Script](scripts/setup-flow-swarm.sh) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with prompt templates, inline shell commands, code snippets, and configuration steps] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes setup and verification instructions, prompt templates, target-selection guidance, and execution cautions for background Claude Code swarm runs.] <br>

## Skill Version(s): <br>
2.1.1 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
