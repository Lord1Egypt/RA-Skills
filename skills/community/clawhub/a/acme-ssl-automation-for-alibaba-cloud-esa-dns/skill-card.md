## Description:

Automatically issue or renew HTTPS certificates using Alibaba Cloud ESA DNS and acme.sh, including apex and wildcard domains, with optional installation to Nginx.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dogeow](https://clawhub.ai/user/dogeow)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and site operators use this skill to issue or renew acme.sh certificates for domains hosted on Alibaba Cloud ESA DNS, especially apex plus wildcard certificates. It also helps prepare DNS-01 validation records and optional Nginx certificate installation or renewal automation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The root cron installer can create high-impact local and credential exposure risk.

Mitigation: Install only on a controlled Linux host after reviewing the installer, and prefer copying the Python script and i18n files into a root-owned directory before enabling cron.

Risk: Long-lived Alibaba Cloud credentials may be exposed through local files, shell history, logs, or chat transcripts.

Mitigation: Use least-privilege RAM or short-lived STS credentials limited to the specific ESA zones, avoid primary account keys, and rotate any credentials that may have been exposed.

Risk: A broad or user-controlled reload command can increase the impact of automated renewal runs.

Mitigation: Limit reload behavior to a fixed Nginx validation and reload command on a controlled host.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/dogeow/skills/acme-ssl-automation-for-alibaba-cloud-esa-dns)
- [Project homepage](https://github.com/dogeow/ali-esa-acme-ssl-skill)
- [acme.sh official project](https://github.com/acmesh-official/acme.sh)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash and Nginx configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include domain-specific certificate issuance commands, environment variable setup, DNS propagation checks, and Nginx certificate path guidance.]

## Skill Version(s):

0.1.4 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
