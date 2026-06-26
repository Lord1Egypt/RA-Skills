## Description: <br>
Manage Cloudflare domains, DNS records, SSL settings, zone configuration, firewall rules, tunnels, and analytics via the Cloudflare API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[InsipidPoint](https://clawhub.ai/user/InsipidPoint) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and site operators use this skill to inspect and manage Cloudflare zones, DNS records, SSL settings, tunnels, cache purges, firewall rules, page rules, and analytics from an agent workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can make privileged changes to Cloudflare DNS, SSL, tunnels, zone settings, cache, and related account resources. <br>
Mitigation: Use a narrowly scoped Cloudflare API token, prefer read-only scopes for inspection, and approve each DNS, SSL, tunnel, settings, import, delete, or full-cache-purge action before execution. <br>
Risk: Destructive or high-impact operations such as deleting DNS records, changing SSL mode, modifying firewall behavior, deleting tunnels, or purging cache can disrupt sites and services. <br>
Mitigation: Follow the artifact's confirmation rules for destructive actions and review command arguments, zone IDs, record IDs, and target domains before running the bundled script. <br>


## Reference(s): <br>
- [Cloudflare API Quick Reference](references/api-guide.md) <br>
- [Cloudflare API Tokens](https://dash.cloudflare.com/profile/api-tokens) <br>
- [ClawHub Skill Page](https://clawhub.ai/InsipidPoint/cloudflare-toolkit) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON API responses from the bundled script] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires CLOUDFLARE_API_TOKEN, curl, jq, and openssl; tunnel operations also require CLOUDFLARE_ACCOUNT_ID.] <br>

## Skill Version(s): <br>
1.5.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
