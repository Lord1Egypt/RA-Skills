## Description:

Creates or updates a proxied Cloudflare DNS A record. Use when you need to programmatically point a subdomain to an IP address. Takes record name, zone name, and IP address as input.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xieyuanqing](https://clawhub.ai/user/xieyuanqing)

### License/Terms of Use:


## Use Case:

Developers and operators use this skill to create or update proxied Cloudflare DNS A records for a specified zone, record name, and IPv4 address during deployment or DNS maintenance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Changing a Cloudflare DNS A record can misdirect traffic if the zone, record name, or IP address is wrong.

Mitigation: Verify the zone, record, and IP address before execution and use a token limited to the intended zone.

Risk: A public-IP lookup example may resolve the machine running the agent rather than the intended target server.

Mitigation: Confirm the target server IP independently before applying DNS changes.

Risk: A broadly scoped Cloudflare API token could change unintended DNS records if exposed or misused.

Mitigation: Use a least-privilege Cloudflare token with DNS edit access only for the required zone and avoid exposing the token in logs or prompts.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/xieyuanqing/skills/cloudflare-dns-updater)
- [Cloudflare zones API endpoint](https://api.cloudflare.com/client/v4/zones?name={args.zone})
- [Cloudflare DNS records API endpoint](https://api.cloudflare.com/client/v4/zones/{zone_id}/dns_records)
- [Public IPv4 lookup example](https://ipv4.icanhazip.com/)

## Skill Output:

**Output Type(s):** [text, json, shell commands, configuration, guidance]

**Output Format:** [Plain text progress messages, JSON DNS record details, and Markdown guidance with inline shell commands.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [No persistent local files are produced by the script.]

## Skill Version(s):

0.1.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
