## Description:

Helps prepare Chinese tender bids by interpreting solicitation documents, generating bid documents, reviewing compliance, and comparing submissions for similarity.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dragonzu](https://clawhub.ai/user/dragonzu)

### License/Terms of Use:

MIT-0

## Use Case:

Bid teams and procurement professionals use the skill to analyze tender requirements, draft bid documents, identify compliance risks, and compare two or three submissions for similarity.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automatic trial provisioning may send device characteristics to the vendor, and account setup may involve phone verification.

Mitigation: Review the trial and account flow first; use a manually obtained API key if you do not want automatic trial provisioning.

Risk: Tender, bid, personal or regulated documents are uploaded to and retained in the vendor cloud.

Mitigation: Upload documents only when authorized to send them to the vendor; remove sensitive material when possible.

Risk: The skill can download documents from supplied URLs and stores an API key in a local configuration file.

Mitigation: Use trusted document URLs, check where the configuration file is saved, and remove credentials on logout or uninstall when needed.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/dragonzu/skills/biaoshu-writer-edu)
- [Usage guide](references/usage.md)
- [API reference](references/api.md)
- [Compliance review API](references/api-compliance.md)
- [Bid similarity API](references/api-duplicate.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Files]

**Output Format:** [Conversational findings and downloadable or locally saved HTML, Word and DOCX documents]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generation, review and similarity checks consume account word credits; bid download links expire.]

## Skill Version(s):

1.0.5 (source: skill frontmatter and server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
