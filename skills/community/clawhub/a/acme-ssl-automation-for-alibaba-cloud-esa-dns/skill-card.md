## Description: <br>
Automatically issues and renews HTTPS certificates with Alibaba Cloud ESA DNS and acme.sh, including wildcard domains and optional Nginx installation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dogeow](https://clawhub.ai/user/dogeow) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operations engineers use this skill to issue or renew certificates for domains hosted on Alibaba Cloud ESA DNS, especially wildcard and apex DNS-01 validation where records must be written to ESA rather than AliDNS. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow requires cloud credentials that can change DNS records. <br>
Mitigation: Use a least-privilege RAM sub-account, prefer short-lived STS credentials, and restrict AccessKey use by IP allowlist. <br>
Risk: Optional certificate installation, reload commands, A-record changes, and cron automation can affect a production host. <br>
Mitigation: Review any --ensure-a-record, --install-cert, --reload-cmd, and cron settings before running. <br>
Risk: Cron renewal can store credentials on the host. <br>
Mitigation: Remove or rotate stored cron credentials when the host is shared or decommissioned. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/dogeow/acme-ssl-automation-for-alibaba-cloud-esa-dns) <br>
- [Publisher profile: dogeow](https://clawhub.ai/user/dogeow) <br>
- [Project homepage](https://github.com/dogeow/ali-esa-acme-ssl-skill) <br>
- [acme.sh](https://github.com/acmesh-official/acme.sh) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce commands that update ESA DNS records, run acme.sh, install certificates, or configure cron renewal.] <br>

## Skill Version(s): <br>
0.1.4 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
