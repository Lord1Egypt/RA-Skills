## Description: <br>
AgentDomains helps agents claim and manage free public hostnames under makes.fyi or agentdomains.co using the AgentDomains CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tashfeenahmed](https://clawhub.ai/user/tashfeenahmed) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill when they need a public hostname for a site, API, webhook callback, redirect, reverse proxy, DNS record, or nameserver delegation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can create, modify, forward, proxy, or delete public DNS names. <br>
Mitigation: Review each AgentDomains command and target before execution, and delete names no longer needed. <br>
Risk: The AgentDomains API key is a secret. <br>
Mitigation: Store AGENTDOMAINS_API_KEY and saved AgentDomains configuration securely, and avoid exposing credentials in shared shells or logs. <br>
Risk: Forwarding or proxying can expose a service publicly or send visitors to an unintended destination. <br>
Mitigation: Confirm the hostname, destination URL, backend, and HTTPS behavior before sharing the public address. <br>


## Reference(s): <br>
- [AgentDomains Documentation](https://docs.agentdomains.co) <br>
- [AgentDomains API Documentation](https://docs.agentdomains.co#api) <br>
- [AgentDomains Service](https://agentdomains.co) <br>
- [AgentDomains CLI Releases](https://github.com/tashfeenahmed/AgentDomains/releases) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with bash command examples and JSON-oriented CLI instructions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May require the AgentDomains CLI, Go for installation, and an AgentDomains API key or saved configuration.] <br>

## Skill Version(s): <br>
0.3.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
