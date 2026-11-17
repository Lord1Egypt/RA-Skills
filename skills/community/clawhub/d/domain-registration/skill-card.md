## Description:

Register, transfer, renew, and secure domains across major provider APIs and dashboards with provider-specific workflows and rollback-safe execution.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ivangdavila](https://clawhub.ai/user/ivangdavila)

### License/Terms of Use:


## Use Case:

External users, developers, and operators use this skill to plan domain registration, transfer, renewal, registrar security, and DNS handoff workflows across major providers. It supports provider-specific API and dashboard paths while requiring confirmation for billing, ownership, WHOIS/contact, transfer, auto-renew, and DNS changes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Registrar workflows can affect billing, ownership, WHOIS/contact records, auto-renew settings, transfers, and DNS service continuity.

Mitigation: Require explicit user confirmation before purchases, transfers, auto-renew changes, WHOIS/contact writes, ownership changes, or DNS changes.

Risk: Registrar credentials or sensitive operational context could be exposed if stored in skill memory files.

Mitigation: Keep registrar credentials outside the skill's memory files and persist only factual operational preferences, inventory, rollback state references, and incident notes.

Risk: Transfer, nameserver, or DNS mutations can disrupt domain resolution if rollback state is incomplete.

Mitigation: Snapshot WHOIS, lock status, nameservers, and DNS records before transfer or DNS changes, then verify outcomes through provider confirmation and resolver-level checks.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/ivangdavila/skills/domain-registration)
- [Skill Homepage](https://clawic.com/skills/domain-registration)
- [Setup - Domain Registration](setup.md)
- [Provider Matrix - Domain Registration](provider-matrix.md)
- [Registration Playbooks](registration-playbooks.md)
- [Transfer and Renewal Operations](transfer-renewal.md)
- [DNS and Registrar Security Controls](dns-security-controls.md)
- [Memory Template - Domain Registration](memory-template.md)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration]

**Output Format:** [Markdown with provider-specific workflow steps, approval checkpoints, and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include registrar API or dashboard action plans, local memory-file updates, rollback notes, and verification commands.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
