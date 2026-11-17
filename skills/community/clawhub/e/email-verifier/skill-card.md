## Description:

Verify email address deliverability via SMTP without sending mail by checking MX records, running RCPT TO verification, and detecting catch-all domains.

This skill is ready for commercial/non-commercial use.

## Publisher:

[psyduckler](https://clawhub.ai/user/psyduckler)

### License/Terms of Use:


## Use Case:

Developers and operators use this skill to validate individual addresses, clean contact lists, and inspect CSV lead lists before outreach. It is intended for authorized verification where live SMTP checks and contact-list privacy obligations are understood.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Live SMTP checks can disclose queried email addresses to external mail servers.

Mitigation: Verify only addresses the user is authorized to check, avoid sensitive contact lists unless privacy obligations are clear, and prefer a constrained runtime for operational use.

Risk: DNS-controlled MX records can steer checks toward unexpected or internal SMTP services.

Mitigation: Run the skill in a restricted network or container that cannot reach internal mail services unless that access is intentional.

Risk: The dependency guidance does not pin dnspython, so installs may change behavior over time.

Mitigation: Pin and review dnspython before production or repeated operational use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/psyduckler/skills/email-verifier)
- [Publisher profile](https://clawhub.ai/user/psyduckler)

## Skill Output:

**Output Type(s):** [text, shell commands, code, guidance]

**Output Format:** [Markdown guidance with shell commands; the verifier script emits JSON results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes deliverability status, MX host, SMTP response details, and error or note fields when available.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
