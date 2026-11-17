## Description:

Manage DigitalOcean resources via API, including Droplets, DNS zones and records, Spaces, Databases, Firewalls, Load Balancers, Kubernetes, and account and billing information.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rexlunae](https://clawhub.ai/user/rexlunae)

### License/Terms of Use:


## Use Case:

Developers and infrastructure operators use this skill to manage DigitalOcean cloud resources from an agent workflow, including server deployment, DNS migration, account inspection, billing lookup, SSH key management, and resource cleanup.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A stored DigitalOcean account token can allow broad changes or deletion of cloud resources.

Mitigation: Use the least-privileged token available and avoid production accounts unless the action is necessary.

Risk: Destructive commands can destroy Droplets, delete DNS records, or delete snapshots and images.

Mitigation: Review destructive commands and target resource identifiers before execution.

Risk: Direct API access can perform operations beyond the reviewed CLI examples.

Mitigation: Be especially cautious with direct API requests and confirm token scope, endpoint, method, and payload before running them.

## Reference(s):

- [DigitalOcean API Reference](https://docs.digitalocean.com/reference/api/)
- [DigitalOcean API Tokens](https://cloud.digitalocean.com/account/api/tokens)
- [DigitalOcean API v2 Base URL](https://api.digitalocean.com/v2/)
- [ClawHub Skill Page](https://clawhub.ai/rexlunae/skills/digitalocean)
- [Publisher Profile](https://clawhub.ai/user/rexlunae)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration instructions, Code, JSON, Guidance]

**Output Format:** [Markdown with bash command examples and JSON command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses a local DigitalOcean API token file and performs live API operations when commands are run.]

## Skill Version(s):

1.0.0 (source: server release metadata, released 2026-02-10)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
