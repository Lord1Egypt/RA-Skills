## Description: <br>
Manage DigitalOcean resources via API, including Droplets, DNS zones and records, Spaces object storage, databases, firewalls, load balancers, Kubernetes, and account or billing information. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[rexlunae](https://clawhub.ai/user/rexlunae) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and infrastructure operators use this skill to inspect and administer DigitalOcean cloud resources from an agent-assisted CLI workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can make powerful DigitalOcean account changes using the user's API token. <br>
Mitigation: Use the narrowest practical API token, protect it on disk, and rotate or revoke it if exposed. <br>
Risk: Create, resize, delete, DNS, billing, and direct API operations can affect live infrastructure or cost. <br>
Mitigation: Require explicit human approval before state-changing, billing-related, or direct API operations. <br>


## Reference(s): <br>
- [DigitalOcean API Reference](https://docs.digitalocean.com/reference/api/) <br>
- [DigitalOcean API Tokens](https://cloud.digitalocean.com/account/api/tokens) <br>
- [DigitalOcean API v2 Base URL](https://api.digitalocean.com/v2/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON API output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands may call the DigitalOcean API and return JSON responses or status messages.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
