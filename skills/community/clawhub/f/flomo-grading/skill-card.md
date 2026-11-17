## Description:

Randomly presents Flomo notes for S/A/B/C/D/E rating, records the user's rating history, and updates personalized note-quality grading principles.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jayshna](https://clawhub.ai/user/jayshna)

### License/Terms of Use:

MIT-0

## Use Case:

Flomo users can use this skill to review random notes, assign personalized quality scores, and refine grading standards over time. It is aimed at personal knowledge management workflows where the agent has access to note content and local scoring files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The package includes note-scoring metadata that the README identifies as private local data.

Mitigation: Install only if broad Flomo note access and local rating-history storage are acceptable; remove scoring-history.json from public packages and provide reset or deletion guidance before treating the release as low risk.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jayshna/skills/flomo-grading)
- [README](artifact/README.md)
- [Skill instructions](artifact/SKILL.md)
- [Grading principles](artifact/grading-principles.md)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Markdown conversation text plus updates to local JSON and Markdown scoring files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires access to Flomo notes and stores local rating history for iterative preference learning.]

## Skill Version(s):

1.4.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
