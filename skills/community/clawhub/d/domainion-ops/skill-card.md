## Description: <br>
Domain and DNS operations across name.com (default), GoDaddy, and Namecheap for registering domains, changing nameservers, managing DNS records, setting up redirects, checking availability, renewals, transfers, and verifying DNS propagation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[iAhmadZain](https://clawhub.ai/user/iAhmadZain) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill to prepare and review domain registrar and DNS administration workflows across name.com, GoDaddy, and Namecheap. It helps with availability checks, registrations, nameserver changes, DNS record updates, redirects, renewals, transfers, and propagation verification. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Live registrar credentials can affect real domains and billing. <br>
Mitigation: Use sandbox accounts where possible, protect API keys, and require explicit review before purchases, renewals, transfers, or auth-code retrieval. <br>
Risk: Nameserver, DNSSEC, forwarding, full-zone replacement, or record deletion changes can disrupt domain availability. <br>
Mitigation: Confirm the domain and provider, list current records first, prefer reversible changes, and verify propagation after each change. <br>
Risk: Incorrect DNS or MX migration guidance can interrupt email or web service delivery. <br>
Mitigation: Keep at least one valid MX record live during migrations and review planned DNS changes before execution. <br>


## Reference(s): <br>
- [name.com API Reference](references/name-com.md) <br>
- [GoDaddy API Reference](references/godaddy.md) <br>
- [Namecheap API Reference](references/namecheap.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/iAhmadZain/domainion-ops) <br>
- [Publisher Profile](https://clawhub.ai/user/iAhmadZain) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, markdown] <br>
**Output Format:** [Markdown with inline bash code blocks and registrar-specific API examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include DNS verification commands and credential setup guidance; should not expose API tokens or secrets.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
