## Description: <br>
Daily Agent is a task orchestration hub that classifies user requests, estimates complexity, routes work to the main session, spawned agents, cron, or specialized skills, and runs final checks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[paudyyin](https://clawhub.ai/user/paudyyin) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and power users use this skill to triage daily work, choose an execution path, select supporting skills, and apply completion checks for routed tasks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can route work toward scheduled jobs, outbound messages, memory writes, background work, and git commits. <br>
Mitigation: Require manual approval before executing scheduled jobs, sending communications, persisting memory, spawning long-running work, or committing files. <br>
Risk: The release security verdict is suspicious because the workflow is broad and highly privileged without clear approval gates. <br>
Mitigation: Review generated commits and persistent tasks before allowing the agent to act, and install only when this orchestration behavior is desired. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/paudyyin/daily-agent) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, markdown] <br>
**Output Format:** [Markdown guidance with routed actions, checklists, and command suggestions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose background execution, scheduled jobs, outbound communications, memory writes, and git commits depending on user request and available agent tools.] <br>

## Skill Version(s): <br>
2.1.0 (source: server release evidence and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
