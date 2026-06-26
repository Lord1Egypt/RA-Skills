## Description: <br>
Security hardening patterns for production AI agents, covering prompt injection defense, data boundary enforcement, read-only integration defaults, write-ahead logging, health checks, integrity gates, rule escalation, and session memory security. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[samledger67-dotcom](https://clawhub.ai/user/samledger67-dotcom) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to harden production AI agent deployments against adversarial inputs, data leaks, and operational failures. It provides policy templates, checklists, and example scripts for agent-level security controls rather than network or infrastructure hardening. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Shell snippets, health-check scripts, cron setup, and monitoring examples may be inappropriate if copied directly into production. <br>
Mitigation: Review and adapt each operational example before use, and make any cron or monitoring setup an explicit operator action. <br>
Risk: The health-check example includes an Anthropic API connectivity check and references an API key. <br>
Mitigation: Decide whether the API call is necessary for the deployment and protect API keys according to local secret-management policy. <br>
Risk: Risky-looking command and exfiltration strings appear in the skill as examples of attacks to block. <br>
Mitigation: Treat attack examples as untrusted illustrative text and avoid executing or copying them as operational commands. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/samledger67-dotcom/agent-security-hardening) <br>
- [Publisher profile](https://clawhub.ai/user/samledger67-dotcom) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown with policy templates, checklists, and shell code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Instruction-only security hardening guidance; examples should be reviewed and adapted before production use.] <br>

## Skill Version(s): <br>
98.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
