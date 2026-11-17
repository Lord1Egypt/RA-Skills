## Description:

Creates, maintains, and validates structured person profiles, including consistent formatting and bidirectional links.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cgartlab](https://clawhub.ai/user/cgartlab)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and knowledge base maintainers use this skill to create or update evidence-grounded person profiles, keep cross-profile links consistent, and validate archive structure and writing rules.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Profile archives or connected accounts may expose private information if shared or published without review.

Mitigation: Review archives for private information and separately approve account connections or publication.

Risk: Bulk migrations or saved lesson and agent-rule edits can alter local archives or agent behavior.

Mitigation: Back up the intended profile folder before bulk changes and review proposed lesson or rule edits.

Risk: A passing validator may be mistaken for proof that profile claims are accurate or formatting is complete.

Mitigation: Independently check sources, factual claims, and formatting; validator success alone does not establish accuracy or full compliance.

## Reference(s):

- [Evidence grading](references/evidence-grading.md)
- [Citation discipline](references/citation-discipline.md)
- [Bidirectional links](references/bidirectional-links.md)
- [Person archive template](templates/person-archive.md)

## Skill Output:

**Output Type(s):** [Markdown, Files, Shell commands]

**Output Format:** [Markdown person profiles, validation reports, and command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Profile templates and local validation scripts support the workflow.]

## Skill Version(s):

0.2.3 (source: release metadata, SKILL.md frontmatter, and CHANGELOG.md; released 2026-10-30)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
