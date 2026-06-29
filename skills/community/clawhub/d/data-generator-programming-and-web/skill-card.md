## Description: <br>
Data Generator - Programming and Web helps agents generate development and testing data including UUIDs, strings, integers, hex values, bytes, passwords, API keys, JWT secrets, colors, emails, IP addresses, Lorem Ipsum text, and timestamps through AgentPMT-hosted remote tool calls. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[agentpmt](https://clawhub.ai/user/agentpmt) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to request random identifiers, mock data, placeholder content, timestamps, and security-sensitive generated strings from the AgentPMT-hosted data generator. It is useful for test data setup, prototyping, mock network records, UI placeholder content, and credential-like development values. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses AgentPMT-hosted remote calls that may spend credits. <br>
Mitigation: Confirm AgentPMT account configuration, enabled tool access, and credit impact before using the skill in automated workflows. <br>
Risk: Generated passwords, API keys, and JWT secrets are sensitive values. <br>
Mitigation: Avoid placing generated secrets in prompts, logs, or shared artifacts, and consider a trusted local generator for high-value production secrets. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/agentpmt/data-generator-programming-and-web) <br>
- [AgentPMT Marketplace Page](https://www.agentpmt.com/marketplace/data-generator-programming-and-web) <br>
- [Generated Action Schema](artifact/schema.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, configuration, guidance] <br>
**Output Format:** [Markdown instructions with JSON request examples and schema tables] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The skill describes 15 AgentPMT-hosted actions whose responses are returned as JSON from the remote tool.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
