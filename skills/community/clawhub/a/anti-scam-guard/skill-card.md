## Description: <br>
Checks URLs from chat, SMS, or email for known scam domains, phishing indicators, and suspicious domain patterns. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[phishguard-niki](https://clawhub.ai/user/phishguard-niki) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, employees, and developers use this skill to check suspicious links before opening them, especially links received through LINE, SMS, or email. It returns risk guidance based on known scam-domain data and domain-pattern checks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Users may over-trust a low-risk result because it means no known match was found, not that the link is guaranteed safe. <br>
Mitigation: Describe low-risk results as no known risk found and advise users to avoid entering sensitive information when the message context still seems suspicious. <br>
Risk: The skill contacts GitHub to fetch threat-data shard files and caches those files locally. <br>
Mitigation: Use the skill only where GitHub access and local caching are acceptable, or pre-download shard data for offline operation when network contact is not desired. <br>
Risk: Broad whitelist behavior can bypass additional checks for some domains and create false confidence. <br>
Mitigation: Treat whitelist-based safe responses as a convenience signal and keep manual review or escalation for unexpected login, payment, wallet, or credential requests. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/phishguard-niki/anti-scam-guard) <br>
- [Publisher profile](https://clawhub.ai/user/phishguard-niki) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown response based on JSON scan results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include per-URL risk levels, matched sources, reasons, and safety guidance.] <br>

## Skill Version(s): <br>
0.4.9 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
