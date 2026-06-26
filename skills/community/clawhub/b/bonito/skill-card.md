## Description: <br>
Onboards users to Bonito for multi-provider AI routing, managed inference, agent deployment, and multi-agent orchestration. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ShabariRepo](https://clawhub.ai/user/ShabariRepo) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and AI platform users use this skill to set up Bonito, create gateway keys, test hosted inference, install bonito-cli, and optionally deploy Bonito agents or the Atlas multi-agent demo. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Gateway keys and provider credentials may be exposed through chat logs, screenshots, source control, or shared terminal output. <br>
Mitigation: Use non-sensitive test prompts and keep Bonito gateway keys and provider credentials out of logs, screenshots, repositories, and shared terminal sessions. <br>
Risk: The optional Atlas demo uses a separate repository and Docker Compose services that may introduce additional configuration and runtime behavior. <br>
Mitigation: Review the Atlas repository and Docker Compose file before running the demo, and run dry-run or prerequisite checks before deployment. <br>


## Reference(s): <br>
- [Bonito docs](https://getbonito.com/docs) <br>
- [Bonito gateway and routing](https://getbonito.com/docs#gateway) <br>
- [Bonito managed inference](https://getbonito.com/docs#managed-inference) <br>
- [Bonito BonBon agents](https://getbonito.com/docs#bonbon) <br>
- [Bonito Bonobot orchestration](https://getbonito.com/docs#bonobot) <br>
- [Bonito MCP integration](https://getbonito.com/docs#mcp) <br>
- [Atlas guide](references/atlas-guide.md) <br>
- [Atlas repository](https://github.com/ShabariRepo/atlas) <br>
- [ClawHub release page](https://clawhub.ai/ShabariRepo/bonito) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with bash, curl, Python, and CLI command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes optional local verification scripts and Bonito/Atlas setup steps.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
