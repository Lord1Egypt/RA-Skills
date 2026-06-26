## Description: <br>
A protocol-layer trust verification skill for AI agents that helps agents check sources, assess intent, scan for prompt injection, and confirm actions before reading, installing, or transacting. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[edvisage](https://clawhub.ai/user/edvisage) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agent developers use this skill to give OpenClaw agents a structured trust-checking routine before they process untrusted content, install skills, or interact with other agents. It provides a manual protocol and memory logging guidance rather than an automatic scanner. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill is a manual protocol rather than an automatic scanner, so protection depends on the agent applying the checklist consistently. <br>
Mitigation: Use it before unknown-source reading, skill installation, and agent transactions, and review the trust-checker log with the owner. <br>
Risk: The skill writes memory entries about detected threats. <br>
Mitigation: Review memory entries for sensitivity, retention expectations, and whether the logged details are appropriate for the agent's operating context. <br>
Risk: Security claims and publisher identity may need confirmation before high-trust use. <br>
Mitigation: Verify the ClawHub publisher profile and release evidence before relying on the skill for security-sensitive decisions. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/edvisage/edvisage-trust-checker) <br>
- [Edvisage AI tools](https://edvisageglobal.com/ai-tools) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, configuration] <br>
**Output Format:** [Markdown guidance with checklist steps and memory-key conventions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write trust-checker:mode and trust-checker:log memory entries when the agent follows the protocol.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata; artifact frontmatter 1.0.1 and package.json 1.0.0 differ) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
