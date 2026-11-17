## Description:

Automates Let's Encrypt SSL certificate issuance, renewal, status checks, and Windows scheduled-task setup using Baidu Intelligent Cloud DNS.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xzhower](https://clawhub.ai/user/xzhower)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and site operators use this skill to configure and operate certificate issuance and renewal for domains hosted on Baidu Intelligent Cloud DNS. It helps an agent provide command guidance for issuing certificates, checking status, renewing certificates, and configuring Windows scheduled renewal.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The package includes an unrelated Gitee upload script with an embedded token and disabled TLS verification.

Mitigation: Remove upload_skill.py before installation, revoke the embedded Gitee token, and keep TLS certificate verification enabled for any future upload tooling.

Risk: The Windows scheduled renewal task is configured to run as SYSTEM with highest privileges.

Mitigation: Run renewal under a dedicated least-privilege account instead of SYSTEM and grant only the filesystem and DNS permissions required for renewal.

Risk: Certificate automation depends on local config.conf secrets, private keys, and an optional post-renewal command.

Mitigation: Protect config.conf and generated private keys, keep them out of public repositories, rotate API keys periodically, and replace RENEW_HOOK with a tightly controlled reload command.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/xzhower/skills/bce-cert-skill-pkg)
- [Documented project code](https://gitee.com/x-hower/bce-cert)
- [Let's Encrypt](https://letsencrypt.org/)
- [Baidu Intelligent Cloud](https://cloud.baidu.com/)
- [acme-tiny reference implementation](https://github.com/diafygi/acme-tiny)

## Skill Output:

**Output Type(s):** [guidance, markdown, shell commands, configuration]

**Output Format:** [Markdown with inline shell commands and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May describe commands that write certificate files, DNS TXT records, logs, and Windows scheduled tasks.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
