## Description:

Converts Bilibili lectures and multi-part courses into Markdown study notes with timed outlines, quoted key points, timestamped transcripts, and one file per course part, using a Bilibili link and optionally a LinkDigest API key.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jackchew7143](https://clawhub.ai/user/jackchew7143)

### License/Terms of Use:

MIT-0

## Use Case:

External learners can turn a Bilibili lecture or multi-part course into study notes with timed outlines, key points, and timestamped transcripts. They can select processing depth and save one Markdown file per course part.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Scanners report that multi-part processing may spend credits before costs and confirmation are clear, and the skill does not declare its tool scope.

Mitigation: Clarify the billing sequence and tool scope before installation or use. Review the total credit estimate and approval step before starting a multi-part run; do not use --yes until the billing flow is understood.

Risk: Partial analysis leaves unresolved whether sensitive environment data could flow to a network request.

Mitigation: Review the skill's network and data handling before installation, and provide only the intended LinkDigest API key rather than unrelated secrets.

## Reference(s):

- [LinkDigest Bilibili course notes](https://linkdigest.dev/zh/bilibili-shipin-biji?ref=skill-bilibili-course-notes)
- [LinkDigest API documentation](https://linkdigest.dev/docs?ref=skill-bilibili-course-notes)
- [LinkDigest pricing](https://linkdigest.dev/pricing)
- [LinkDigest privacy policy](https://linkdigest.dev/privacy)

## Skill Output:

**Output Type(s):** [Markdown, Files]

**Output Format:** [Markdown study notes with timed outlines, key points, and timestamped transcripts; multi-part courses produce one file per part.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Output depth and whether on-screen text is included depend on the selected options.]

## Skill Version(s):

1.0.0 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
