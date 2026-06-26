## Description: <br>
Audit and improve email deliverability for ecommerce marketing by diagnosing spam folder issues, list hygiene problems, authentication gaps, and sending reputation issues. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[leooooooow](https://clawhub.ai/user/leooooooow) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External ecommerce marketers and deliverability consultants use this skill to audit inbox placement, authentication, list hygiene, content quality, sender reputation, and monitoring practices for email campaigns. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Deliverability audits can involve privacy-sensitive subscriber, campaign, ESP, and domain data. <br>
Mitigation: Use read-only ESP access where possible, export only fields needed for the audit, and limit sharing with approved list-verification and DMARC vendors. <br>
Risk: Incorrect authentication or DMARC changes can affect legitimate email delivery. <br>
Mitigation: Stage DNS and policy changes, validate SPF, DKIM, and DMARC before enforcement, and monitor aggregate reports before moving to stricter policies. <br>
Risk: DMARC forensic reporting and third-party verification tools may expose email or subscriber data. <br>
Mitigation: Avoid enabling forensic reporting unless privacy or legal review approves it, and use vendors approved for the data being processed. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/leooooooow/email-deliverability) <br>
- [Email Authentication Setup Guide](authentication-setup-guide.md) <br>
- [Email List Hygiene Guide](list-hygiene-guide.md) <br>
- [Email Deliverability Quality Checklist](quality-checklist.md) <br>
- [Email Deliverability Audit Report Template](output-template.md) <br>
- [Google Postmaster Tools](https://postmaster.google.com) <br>
- [MXToolbox](https://mxtoolbox.com) <br>
- [dmarcian](https://dmarcian.com) <br>
- [mail-tester.com](https://www.mail-tester.com) <br>
- [Spamhaus](https://www.spamhaus.org) <br>
- [RFC 7489: DMARC](https://datatracker.ietf.org/doc/html/rfc7489) <br>
- [M3AAWG Published Documents](https://www.m3aawg.org/published-documents) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration, guidance] <br>
**Output Format:** [Markdown audit reports, checklists, status matrices, and prioritized remediation plans.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include domain, ESP, campaign metrics, subscriber list segments, DNS authentication status, and remediation timelines supplied by the user.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
