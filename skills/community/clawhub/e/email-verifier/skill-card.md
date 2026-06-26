## Description: <br>
Verify email address deliverability via SMTP without sending mail, including MX lookup, RCPT TO verification, catch-all detection, single-address checks, batch checks, and CSV input. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[psyduckler](https://clawhub.ai/user/psyduckler) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, operators, and data-quality workflows use this skill to check whether email addresses appear deliverable before outreach or record cleanup. It is best suited for authorized, low-volume validation where live SMTP probing is acceptable. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Live SMTP verification can disclose queried email addresses and source IP metadata to recipient mail servers. <br>
Mitigation: Use it only for addresses you own or are authorized to process, and prefer syntax or domain-only checks when privacy or mail-server reputation matters. <br>
Risk: Rapid or high-volume SMTP checks can damage IP reputation, trigger greylisting, or lead to port 25 blocks. <br>
Mitigation: Keep batch sizes conservative, use the documented rate limits, and use a dedicated email verification service for bulk lists. <br>
Risk: Catch-all domains, greylisting, and servers that block verification can make results inconclusive. <br>
Mitigation: Treat catch-all and unknown results as uncertain rather than proof that an inbox exists. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/psyduckler/email-verifier) <br>


## Skill Output: <br>
**Output Type(s):** [shell commands, code, configuration, text] <br>
**Output Format:** [Markdown guidance with shell commands and JSON array results from the verifier script] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Results include email, domain, MX host, SMTP code and response, deliverability status, and optional error or note fields.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
