## Description:

AI QA Agent reviews code, data, brand voice, and document formatting to produce a pass/fail QA report with specific findings before delivery.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mattsteff-hope](https://clawhub.ai/user/mattsteff-hope)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill as a final QA gate before delivery or sign-off. It reviews deliverables across code correctness, data integrity, brand voice, and document formatting, then returns an actionable QA report.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may inspect deliverables provided for review and may persist a QA report under /home/z/my-project/download.

Mitigation: Use it only when that file access and report persistence are acceptable.

Risk: Vague review requests can lead the skill to inspect a broader deliverable scope than intended.

Mitigation: Manually confirm the review scope when the request is ambiguous.

## Reference(s):

- [Brand Voice Guide](artifact/brand-voice-guide.md)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown QA report]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May save a QA report under /home/z/my-project/download.]

## Skill Version(s):

1.0.0 (source: server release metadata and changelog)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
