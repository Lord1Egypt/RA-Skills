## Description: <br>
Configure DNS records correctly with proper TTLs, email authentication, and migration strategies. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ivangdavila](https://clawhub.ai/user/ivangdavila) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and site operators use this skill to plan DNS changes, configure email authentication and certificate-related records, and troubleshoot resolver behavior. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Incorrect DNS record changes can affect website availability, email delivery, or certificate issuance. <br>
Mitigation: Apply recommendations deliberately in the DNS provider, lower TTLs before migrations, and verify authoritative and cached responses after changes. <br>
Risk: Provider-specific DNS behavior can differ from general guidance. <br>
Mitigation: Confirm provider behavior before applying changes, especially for proxying, apex CNAME flattening, TTL handling, and wildcard or certificate records. <br>


## Reference(s): <br>
- [ClawHub DNS skill page](https://clawhub.ai/ivangdavila/dns) <br>
- [ClawHub publisher profile: ivangdavila](https://clawhub.ai/user/ivangdavila) <br>
- [Mail Tester](https://www.mail-tester.com/) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline DNS record examples and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Documentation-only guidance; no executable files or hidden behavior were found in the security scan.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
