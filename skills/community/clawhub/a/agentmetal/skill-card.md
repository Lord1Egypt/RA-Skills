## Description: <br>
Clawhub helps an agent provision and manage real Linux VPS instances through AgentMetal, including paid USDC or card provisioning, SSH access, command execution, storage add-ons, lease extension, diagnostics, reboot, and destroy workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[luiscosio](https://clawhub.ai/user/luiscosio) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, operators, and autonomous agents use this skill to rent short-lived Linux servers, inspect available plans, manage leases, run commands on owned servers, and host or deploy services without a separate cloud dashboard. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can initiate paid VPS provisioning, lease extensions, and paid add-ons. <br>
Mitigation: Require explicit approval before payment, lease extension, or add-on actions, and keep per-request spending caps low. <br>
Risk: The skill handles sensitive credentials such as wallet private keys, AgentMetal API keys, and SSH private keys. <br>
Mitigation: Scope credentials tightly, avoid exposing private keys in logs, and prefer supplying an existing SSH public key instead of receiving a generated private key. <br>
Risk: The skill can run root commands and destroy managed servers. <br>
Mitigation: Require explicit approval before root exec or destroy operations and review commands before execution. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/luiscosio/agentmetal) <br>
- [AgentMetal homepage](https://agentmetal.dev) <br>
- [AgentMetal agent-facing manual](https://api.agentmetal.dev/llms.txt) <br>
- [AgentMetal catalog endpoint](https://api.agentmetal.dev/v1/catalog) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, code] <br>
**Output Format:** [Markdown with shell commands, API examples, and CLI configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May invoke external AgentMetal API calls through curl or the bundled CLI; paid operations require explicit wallet or card payment flow and sensitive credentials.] <br>

## Skill Version(s): <br>
0.2.0 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
