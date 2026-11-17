## Description:

Vets papers shared in meetings, seminars, or reading clubs by checking citation authenticity, reproducibility signals, and image-integrity concerns before the group commits time to reading.

This skill is ready for commercial/non-commercial use.

## Publisher:

[j-levee](https://clawhub.ai/user/j-levee)

### License/Terms of Use:

MIT-0

## Use Case:

Researchers, students, and meeting participants use this skill to triage a shared paper before deep reading. It produces an evidence-backed credibility report covering references, reproducibility, image-integrity checks when images are provided, and reading recommendations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow may process meeting transcripts, recordings, participant names, and paper-sharing context.

Mitigation: Require explicit participant consent before use, avoid full recordings unless necessary, and redact speaker names when sharing reports.

Risk: Default local usage logging could retain method-level usage details without enough retention controls.

Mitigation: Disable or clarify local logging before deployment and define retention expectations for any logs that remain enabled.

## Reference(s):

- [Coverage Dimensions](references/coverage.md)
- [Credibility Report Template](references/credibility-report.md)
- [ClawHub Skill Page](https://clawhub.ai/j-levee/skills/cjg-paper-fact-checker)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown credibility report with evidence links, section ratings, an overall high/medium/low rating, and meeting-oriented reading recommendations.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May reference citation-check results, reproducibility gaps, image-comparison findings when supplied, and participant attribution from meeting context.]

## Skill Version(s):

2.0.1 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
