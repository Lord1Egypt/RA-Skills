## Description:

Restyles an existing BII-format single-stock briefing in a BlackRock Investment Institute-inspired visual style and exports matching HTML, PDF, and PPTX files without changing its visible report content.

This skill is for research and development only.

## Publisher:

[yjkj999999](https://clawhub.ai/user/yjkj999999)

### License/Terms of Use:

MIT-0

## Use Case:

Analysts and developers with an existing BII-format stock briefing use this skill to apply a consistent institutional-style layout and deliver the same report as HTML, PDF, and a presentation deck. It changes presentation, not the underlying investment analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: BlackRock-inspired styling could be mistaken for an official BlackRock publication or used without permission.

Mitigation: Confirm the right to use the visual identity and review the independent-publication statement and final outputs before distribution.

Risk: PPTX speaker notes contain hidden, searchable report text copied from the PDF.

Mitigation: Inspect or remove notes before sharing a deck with recipients who should not receive that text.

Risk: Exports can overwrite earlier files in an output directory.

Mitigation: Use a fresh output directory for each run.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/yjkj999999/skills/bii-blackrock-note)

## Skill Output:

**Output Type(s):** [Files]

**Output Format:** [HTML, PDF, and PPTX]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The PPTX uses slide images with searchable speaker notes rather than editable slide text; an existing BII HTML report is required.]

## Skill Version(s):

1.1.0 (source: SKILL.md frontmatter and ClawHub release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
