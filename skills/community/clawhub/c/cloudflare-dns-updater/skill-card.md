## Description: <br>
Creates or updates a proxied Cloudflare DNS A record. Use when you need to programmatically point a subdomain to an IP address. Takes record name, zone name, and IP address as input. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xieyuanqing](https://clawhub.ai/user/xieyuanqing) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and infrastructure operators use this skill to create or update Cloudflare DNS A records for a specified zone, record name, IP address, and proxy setting during deployment or DNS management workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can make live Cloudflare DNS changes using an API token. <br>
Mitigation: Use a least-privilege Cloudflare API token scoped to the intended zone and confirm the zone, record, IP address, and proxied setting before execution. <br>
Risk: The Cloudflare API token could be exposed through shared logs or shell history. <br>
Mitigation: Set CLOUDFLARE_API_TOKEN through the host environment or a secret manager and avoid echoing it in commands or logs. <br>


## Reference(s): <br>
- [Cloudflare Dns Updater on ClawHub](https://clawhub.ai/xieyuanqing/cloudflare-dns-updater) <br>
- [README.md](artifact/README.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON output from the DNS update script] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The script prints progress messages and, on success, the created or updated Cloudflare DNS record as formatted JSON.] <br>

## Skill Version(s): <br>
0.1.1 (source: release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
