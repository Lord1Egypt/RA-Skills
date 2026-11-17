## Description:

Generates AI agent security advisories with threat analysis, severity scoring, MITRE ATT&CK mapping, and remediation guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[krishnakumarmahadevan-cmd](https://clawhub.ai/user/krishnakumarmahadevan-cmd)

### License/Terms of Use:

MIT-0

## Use Case:

Security teams and developers use this skill to generate AI-agent threat advisories for prompt injection, data leakage, model manipulation, and unauthorized access scenarios, including severity, MITRE ATT&CK mapping, and remediation guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: AI-agent security scenarios, environment details, capabilities, existing controls, impact, and sensitivity labels are sent to ToolWeb's third-party API.

Mitigation: Use only with approval for the data being shared, and do not submit secrets, regulated data, customer data, internal hostnames, or confidential incident details unless the provider's privacy and retention terms are acceptable.

Risk: The skill has no local fallback and instructs the agent to depend on the ToolWeb API for advisory generation.

Mitigation: Treat API availability and response quality as external dependencies, and review returned advisories before using them for security decisions.

Risk: Successful API calls may incur billable usage under the publisher's plans.

Mitigation: Configure API keys only for authorized accounts, monitor usage, and apply rate or budget controls where available.

## Reference(s):

- [AgentSecly ClawHub listing](https://clawhub.ai/krishnakumarmahadevan-cmd/skills/agentsecly-ai-agent-security)
- [ToolWeb API Hub](https://portal.toolweb.in)
- [AgentSecly API endpoint](https://portal.toolweb.in/apis/security/agentsecly)
- [ToolWeb platform](https://toolweb.in)
- [ToolWeb OpenClaw skills](https://toolweb.in/openclaw/)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown advisory with structured severity, MITRE mapping, threat analysis, affected agent profiles, remediation actions, and recommended security controls.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires TOOLWEB_API_KEY and curl; successful API calls may be billable under the publisher's subscription plans.]

## Skill Version(s):

1.0.2 (source: server release metadata; artifact frontmatter lists 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
