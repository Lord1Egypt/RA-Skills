## Description:

Prepares a draft U.S. CBP entry summary for commercial import shipments, including entry-type selection, document review, HTS confirmation, duty and fee estimates, PGA screening, and line-item summary drafting for licensed customs-broker review.

This skill is ready for commercial/non-commercial use.

## Publisher:

[archlab-space](https://clawhub.ai/user/archlab-space)

### License/Terms of Use:

MIT-0

## Use Case:

Licensed customs brokers, import compliance managers, trade-compliance teams, in-house trade counsel, and freight forwarders use this skill to assemble a draft U.S. import entry package for broker review before any ACE/ABI transmission.

### Deployment Geography for Use:

United States

## Known Risks and Mitigations:

Risk: Importer tax/account details, bill of lading data, and commercial invoices can contain sensitive business information.

Mitigation: Use only in an agent session approved for that data and redact fields that are not needed for drafting.

Risk: Draft duty, fee, classification, and PGA outputs may be incomplete or outdated if treated as final filing guidance.

Mitigation: Require review by a licensed customs broker or trade counsel before relying on the draft or making any ACE/ABI submission.

Risk: Fee caps, duty rates, trade remedies, sanctions, and agency admissibility requirements can change.

Mitigation: Confirm current CBP, HTSUS, OFAC, AD/CVD, Section 301/232, and PGA requirements before finalizing the entry.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/archlab-space/skills/customs-entry-drafter)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown with structured tables, checklists, estimates, and review notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Draft-only output labeled for licensed customs-broker review; it does not transmit filings.]

## Skill Version(s):

0.1.0 (source: changelog, released 2026-05-30; server release version 0.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
