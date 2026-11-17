## Description:

Turns a fact-checked, compliance-approved Markdown draft into multi-channel publishing assets and an archive record without repeating fact-checking or publishing automatically.

This skill is ready for commercial/non-commercial use.

## Publisher:

[haiyangchenbj](https://clawhub.ai/user/haiyangchenbj)

### License/Terms of Use:

MIT-0

## Use Case:

Content publishers and editors use this skill to turn an already reviewed final draft into WeChat, LinkedIn, and standalone HTML assets, plus an archive record. It expects upstream fact-checking and approval to be complete.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security scan was partial and did not inspect every artifact reference or component; the skill includes executable scripts.

Mitigation: Review the scripts and referenced files before use, and run the included output validators.

Risk: Publishing assets rely on the input draft having completed fact-checking and compliance review.

Mitigation: Confirm the required approval gate before generating assets; return new factual claims to upstream review.

Risk: LinkedIn output has an English-source and review prerequisite that can limit what the skill can produce.

Mitigation: Complete the English source and its claim-map and authorship review before creating LinkedIn content.

## Reference(s):

- [Channel output contracts](references/channel-contracts.md)
- [WeChat inline-style guidance](references/wechat-style.md)
- [WeChat layout baseline](references/wechat_layout_baseline.json)

## Skill Output:

**Output Type(s):** [Markdown, HTML, JSON, JPEG image]

**Output Format:** [Multi-file publishing package with channel content, archive records, and summary-card artwork.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Based on a reviewed final draft; includes validation reports and does not perform external publishing.]

## Skill Version(s):

1.1.16 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
