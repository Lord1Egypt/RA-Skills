## Description: <br>
Comprehensive Gandi domain registrar integration for domain and DNS management, including domain registration and renewal, DNS record management, email forwarding, SSL certificate checks, DNS snapshots, and bulk zone operations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chrisagiddings](https://clawhub.ai/user/chrisagiddings) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, domain administrators, and technical operators use this skill to inspect and manage Gandi domains, DNS records, email forwarding, certificates, DNSSEC, snapshots, and registrar workflows from an agent-assisted command environment. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Write-scoped Gandi tokens can authorize DNS, email, domain, certificate, and renewal actions that affect live services or create financial transactions. <br>
Mitigation: Use the minimum required token scopes, prefer separate read-only and write tokens, and install only when comfortable granting the selected Gandi permissions. <br>
Risk: Bulk DNS, snapshot restore, DNSSEC, email-forwarding, registration, renewal, certificate, and force-mode commands can disrupt websites, mail delivery, or account state. <br>
Mitigation: Review commands before execution, avoid force options unless intentional, test on non-production domains where possible, and create DNS snapshots before changes. <br>
Risk: Credential exposure can occur if tokens are printed, committed, stored in shell profiles, or shared across workflows. <br>
Mitigation: Store tokens in secured files with owner-only permissions or managed environment secrets, rotate tokens regularly, and revoke unused tokens. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/chrisagiddings/gandi-skill) <br>
- [Gandi API Overview](references/api-overview.md) <br>
- [Authentication](references/authentication.md) <br>
- [Setup Guide](references/setup.md) <br>
- [Domain Management API](references/domains.md) <br>
- [LiveDNS Management API](references/livedns.md) <br>
- [Scripts Reference](SCRIPTS.md) <br>
- [Official Gandi API Documentation](https://api.gandi.net/docs/) <br>
- [Gandi Personal Access Tokens](https://admin.gandi.net/organizations/account/pat) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, API Calls, JSON] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Node.js, npm, and a Gandi Personal Access Token provided through GANDI_API_TOKEN or a secured local token file.] <br>

## Skill Version(s): <br>
0.2.7 (source: server release metadata, SKILL.md openclaw metadata, CHANGELOG) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
