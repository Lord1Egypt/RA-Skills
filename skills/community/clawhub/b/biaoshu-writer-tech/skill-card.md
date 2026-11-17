## Description:

Helps procurement teams interpret tender documents, draft bid submissions, review compliance, and compare bids for similarity through a cloud service.

This skill is ready for commercial/non-commercial use.

## Publisher:

[liu-jiapeng](https://clawhub.ai/user/liu-jiapeng)

### License/Terms of Use:

MIT-0

## Use Case:

Procurement and bid-writing teams use this skill to assess tender requirements, prepare bid documents, review compliance issues, and compare legally held submissions for similarity.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Tender and bid documents are transferred to the vendor cloud, potentially exposing confidential procurement material.

Mitigation: Use only files authorized for external processing; confirm the vendor's retention, deletion, and data-use terms before submitting sensitive material.

Risk: API keys may be stored locally or pasted into chat.

Mitigation: Avoid sharing keys in chat where possible, restrict access to stored credentials, and rotate keys if exposed.

Risk: Trial and account setup may collect device information and phone or SMS details.

Mitigation: Review account enrollment and data-collection terms before starting a trial or registering.

Risk: Generation, review, and similarity checks may incur paid usage; automated assessments may need verification.

Mitigation: Review billing terms and available balance before paid tasks, and have a qualified reviewer check conclusions before relying on them.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/liu-jiapeng/skills/biaoshu-writer-tech)
- [Bailian bid-writing service](https://biaoshu.zhiliaobiaoxun.com/)
- [Usage workflow](artifact/references/usage.md)
- [API documentation](artifact/references/api.md)
- [Bid similarity documentation](artifact/references/api-duplicate.md)

## Skill Output:

**Output Type(s):** [Text, Guidance, Files]

**Output Format:** [Markdown responses and generated HTML, DOCX, or JSON results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Bid documents may be delivered by short-lived download link; reports can be saved locally.]

## Skill Version(s):

2.0.6 (source: server release and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
