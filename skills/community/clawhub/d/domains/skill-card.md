## Description:

Register, manage, and protect domain names with practical DNS and security guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ivangdavila](https://clawhub.ai/user/ivangdavila)

### License/Terms of Use:


## Use Case:

External users, developers, and operators use this skill for practical guidance on registering, configuring DNS for, transferring, and protecting domain names.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Registrar credentials and EPP authorization codes are sensitive; mishandling them can enable unauthorized domain transfers or account compromise.

Mitigation: Treat registrar credentials and EPP codes like secrets, use two-factor authentication, keep registrar lock enabled, and share transfer codes only through trusted channels.

Risk: DNS record changes can interrupt web or email service if records, TTLs, or migration timing are wrong.

Mitigation: Plan DNS migrations, lower TTLs before changes, verify A, CNAME, MX, and DNSSEC settings, and keep rollback details available.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ivangdavila/skills/domains)
- [ClawHub publisher profile](https://clawhub.ai/user/ivangdavila)

## Skill Output:

**Output Type(s):** [Guidance, Text, Configuration]

**Output Format:** [Markdown guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Static informational guidance; no tool, credential, persistence, or elevated-access behavior is requested.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
