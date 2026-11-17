## Description:

Helps prepare bids by interpreting tender documents, generating DOCX proposals, reviewing compliance, and comparing bid documents for similarity.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dragonzu](https://clawhub.ai/user/dragonzu)

### License/Terms of Use:

MIT-0

## Use Case:

Bidding teams and other external users can interpret tender requirements, draft proposal documents, review compliance risks, and compare two or three bids for similarity before submission.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Tender and bid files are sent to a vendor cloud for processing and may contain confidential business information.

Mitigation: Obtain authorization before uploading files and avoid sending documents that cannot be shared with the vendor.

Risk: The automatic trial collects device fingerprint details, and registration can collect phone and SMS data, despite the stated permissions excluding these categories.

Mitigation: Review the data practices before installation; use an explicit website-issued API key instead of automatic trial registration if device fingerprint collection is unacceptable.

Risk: Generated bids and similarity or compliance findings can be incomplete or mistaken; paid operations consume account credits.

Mitigation: Confirm costs and review the generated documents and findings with a qualified person before relying on them or submitting a bid.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/dragonzu/skills/biaoshu-writer-service)
- [Service website](https://biaoshu.zhiliaobiaoxun.com/?ch=s97)
- [API overview](artifact/references/api.md)
- [Usage guide](artifact/references/usage.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Files, Guidance]

**Output Format:** [Conversational summaries, HTML reports, DOCX proposals, and JSON results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated files may be delivered through short-lived download links; generation, review, and similarity checks can consume account credits.]

## Skill Version(s):

1.0.5 (source: skill frontmatter and ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
