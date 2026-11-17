## Description:

Generates detailed daily, weekly, or monthly work summaries for managers, saving to memory and exporting reports as HTML or PDF.

This skill is ready for commercial/non-commercial use.

## Publisher:

[linux2010](https://clawhub.ai/user/linux2010)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and other workers use this skill to compile daily, weekly, or monthly summaries of recent work for managers, including completed tasks, project progress, issues, metrics, and next plans.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may gather broad private work, memory, session, and system data.

Mitigation: Use it only for explicitly requested reports and restrict collection to selected projects and date ranges.

Risk: Reports may include secrets, personal data, or sensitive session content.

Mitigation: Redact secrets and personal data, and avoid session transcripts and long-term memory unless necessary.

Risk: Generated HTML or PDF reports may persist or expose sensitive work details.

Mitigation: Preview reports before saving or sharing and treat generated HTML/PDF files as sensitive.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/linux2010/skills/boss-report)
- [SKILL.md](artifact/SKILL.md)
- [report-generator.js](artifact/report-generator.js)

## Skill Output:

**Output Type(s):** [text, markdown, files, guidance]

**Output Format:** [Markdown reports, chat summaries, and generated HTML or PDF report files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May persist reports to memory files and export HTML/PDF when requested.]

## Skill Version(s):

1.0.0 (source: release evidence, released 2026-04-20)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
