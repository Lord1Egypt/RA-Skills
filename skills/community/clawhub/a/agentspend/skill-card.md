## Description: <br>
AgentSpend helps agents discover external paid services, configure spending controls, and call paid APIs through the agentspend CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jpbonch](https://clawhub.ai/user/jpbonch) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent operators use AgentSpend to discover paid API services, check prices, and make controlled paid HTTP requests when built-in tools are insufficient. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can let an agent make paid external API requests. <br>
Mitigation: Use it only when paid API access is intended, require user approval for paid requests, and set a low weekly budget before use. <br>
Risk: A broad service-search and payment workflow can reach unintended domains or services. <br>
Mitigation: Configure a strict domain allowlist and use the check command before pay to confirm price and request shape. <br>
Risk: Requests may expose sensitive headers or body content to external services. <br>
Mitigation: Do not send secrets in headers or bodies, and review each request before running agentspend pay. <br>
Risk: The local AgentSpend credential grants spending authority while it remains valid. <br>
Mitigation: Protect the local credential file and revoke the credential when AgentSpend is no longer needed. <br>


## Reference(s): <br>
- [AgentSpend ClawHub Page](https://clawhub.ai/jpbonch/agentspend) <br>
- [Publisher Profile](https://clawhub.ai/user/jpbonch) <br>
- [README](README.md) <br>
- [Skill Instructions](SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and CLI output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include paid API response bodies, charge amounts, and remaining weekly budget information.] <br>

## Skill Version(s): <br>
0.1.3 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
