## Description:

Audit and improve email deliverability for ecommerce marketing by diagnosing spam folder issues, list hygiene problems, authentication gaps, and sending reputation issues.

This skill is ready for commercial/non-commercial use.

## Publisher:

[leooooooow](https://clawhub.ai/user/leooooooow)

### License/Terms of Use:

MIT-0

## Use Case:

Ecommerce marketers, deliverability consultants, and operators use this skill to audit sender reputation, authentication, list hygiene, content quality, and sending infrastructure, then produce prioritized remediation and monitoring plans.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Subscriber-list exports can expose customer data to unnecessary parties or services.

Mitigation: Confirm authorization before exporting customer data, share only the minimum fields needed, and review privacy and data-processing terms for any verification vendor.

Risk: DNS authentication changes can disrupt legitimate email if applied without review.

Mitigation: Get approval and backups before changing SPF, DKIM, DMARC, BIMI, return-path, or sending-domain records, and validate changes with trusted testing tools.

Risk: Bulk suppressions or removals can remove reachable subscribers or break compliance retention records.

Mitigation: Review suppression criteria before execution, keep required suppression records, and preserve backups before bulk list changes.

## Reference(s):

- [Email Authentication Setup Guide](artifact/authentication-setup-guide.md)
- [Email List Hygiene Guide](artifact/list-hygiene-guide.md)
- [Email Deliverability Audit Report Template](artifact/output-template.md)
- [Email Deliverability Quality Checklist](artifact/quality-checklist.md)
- [Google Postmaster Tools](https://postmaster.google.com)
- [MXToolbox](https://mxtoolbox.com)
- [dmarcian](https://dmarcian.com)
- [mail-tester.com](https://www.mail-tester.com)
- [Spamhaus](https://www.spamhaus.org)
- [RFC 7489: Domain-based Message Authentication, Reporting, and Conformance](https://datatracker.ietf.org/doc/html/rfc7489)
- [M3AAWG Published Documents](https://www.m3aawg.org/published-documents)

## Skill Output:

**Output Type(s):** [text, markdown, guidance, configuration]

**Output Format:** [Markdown reports, checklists, matrices, and remediation plans with DNS and ESP configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May recommend use of external deliverability, verification, blacklist, rendering, and DNS validation tools.]

## Skill Version(s):

1.1.0 (source: server release metadata; artifact frontmatter says 1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
