## Description: <br>
Register, transfer, renew, and secure domains across major provider APIs and dashboards with provider-specific workflows and rollback-safe execution. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ivangdavila](https://clawhub.ai/user/ivangdavila) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and domain operations teams use this skill to plan and execute domain registrations, transfers, renewals, DNS handoffs, and registrar hardening across supported providers with explicit approvals for billing and ownership changes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Domain lifecycle actions can affect billing, ownership, renewal status, and service continuity. <br>
Mitigation: Require explicit confirmation for billing and ownership writes, verify exact domains and renewal pricing, and run one-domain pilots before batch operations. <br>
Risk: Registrar credentials, API keys, and recovery codes could expose domain ownership if stored in operational notes. <br>
Mitigation: Use least-privilege provider credentials and keep passwords, API keys, and recovery codes out of ~/domain-registration/. <br>
Risk: DNS or nameserver changes can cause outages or failed recovery during transfers and migrations. <br>
Mitigation: Snapshot DNS and nameserver state before changes, validate outcomes with provider confirmations plus dig and WHOIS checks, and keep rollback-ready records. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ivangdavila/domain-registration) <br>
- [Skill homepage](https://clawic.com/skills/domain-registration) <br>
- [Skill definition](artifact/SKILL.md) <br>
- [Provider matrix](artifact/provider-matrix.md) <br>
- [Registration playbooks](artifact/registration-playbooks.md) <br>
- [Transfer and renewal operations](artifact/transfer-renewal.md) <br>
- [DNS and registrar security controls](artifact/dns-security-controls.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance with provider-specific checklists and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May reference local operational memory under ~/domain-registration/ and registrar API or dashboard workflows selected by the user.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
