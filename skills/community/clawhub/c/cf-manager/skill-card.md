## Description: <br>
Manage Cloudflare via API: DNS zones and records, page rules, SSL/TLS settings, caching, firewall rules, Workers, and analytics. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[rexlunae](https://clawhub.ai/user/rexlunae) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and infrastructure operators use this skill to inspect and manage Cloudflare resources from an agent-assisted command-line workflow, including DNS, zones, SSL/TLS, cache purges, firewall rules, Workers, and analytics. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can make production-impacting Cloudflare changes, including DNS, SSL/TLS, firewall, cache purge, Worker, and delete operations. <br>
Mitigation: Require human review before executing production-impacting commands and scope API tokens to only the zones and permissions needed. <br>
Risk: Cloudflare API tokens grant access to infrastructure resources and could be exposed through logs, synced folders, or overly broad storage. <br>
Mitigation: Store tokens in a protected local config file, keep them out of logs and synced folders, and prefer least-privilege tokens. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/rexlunae/cf-manager) <br>
- [Cloudflare API reference](https://developers.cloudflare.com/api/) <br>
- [Cloudflare API v4 base URL](https://api.cloudflare.com/client/v4/) <br>
- [Cloudflare API token management](https://dash.cloudflare.com/profile/api-tokens) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, JSON, Guidance] <br>
**Output Format:** [Markdown guidance with bash command examples and JSON API output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a Cloudflare API token stored outside the skill artifact.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
