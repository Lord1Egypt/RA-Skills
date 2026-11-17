## Description:

Tracks reading, including books in progress, notes, themes across completed books, reading goals, and recommendations for what to read next.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rednix](https://clawhub.ai/user/rednix)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to maintain a private reading library, capture notes and reflections, manage a reading list, and receive recommendations based on their reading history and preferences.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Reading history and notes can contain private personal interests, reflections, and quotes.

Mitigation: Keep reading lists and notes in the owner's private channel, as specified by the artifact privacy rules.

Risk: Book-related casual phrases may invoke the skill unexpectedly.

Mitigation: Confirm user intent before adding, removing, exporting, or changing book records.

Risk: Optional knowledge-base export can make selected reading notes searchable outside the book tracker.

Mitigation: Only export notes to a knowledge base after explicit user approval.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/rednix/skills/book-tracker)
- [OpenClaw skill homepage](https://clawhub.com/skills/book-tracker)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance, Configuration]

**Output Format:** [Markdown with structured book entries, reading-list updates, notes, reflections, and recommendation text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update private library.md, reading-list.md, and config.md content when the user instructs it.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
