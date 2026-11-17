## Description:

Domainion Ops guides domain and DNS operations across name.com, GoDaddy, and Namecheap, including domain registration, nameserver changes, DNS records, redirects, availability checks, renewals, transfers, and propagation verification.

This skill is ready for commercial/non-commercial use.

## Publisher:

[iahmadzain](https://clawhub.ai/user/iahmadzain)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to plan and execute registrar and DNS operations across name.com, GoDaddy, and Namecheap accounts. It supports domain availability checks, registrations, renewals, transfers, nameserver changes, DNS record management, redirects, and propagation verification.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can make high-impact registrar changes such as purchases, renewals, DNS replacements, nameserver changes, unlocks, and transfer-code requests.

Mitigation: Use sandbox accounts first and require explicit user confirmation before any purchase, renewal, DNS replacement, nameserver change, unlock, or transfer-code request.

Risk: Registrar credentials may be exposed through visible commands, logs, or command traces.

Mitigation: Store credentials with restrictive permissions, avoid pasting production secrets into visible commands, and rotate any registrar keys that may have appeared in logs or traces.

Risk: A wrong provider, wrong registrar, duplicate DNS record, or unsafe MX migration can cause outages or failed changes.

Mitigation: Confirm the domain and provider, list existing records before changes, keep at least one valid MX record live during migrations, and verify results after each change.

## Reference(s):

- [name.com API Reference](artifact/references/name-com.md)
- [GoDaddy API Reference](artifact/references/godaddy.md)
- [Namecheap API Reference](artifact/references/namecheap.md)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration]

**Output Format:** [Markdown with inline shell commands and provider-specific API request examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include provider selection, credential setup guidance, confirmation prompts, DNS verification steps, and registrar API calls.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
