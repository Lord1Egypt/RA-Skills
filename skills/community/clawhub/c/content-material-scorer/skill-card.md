## Description:

Scores short video and talking-head content ideas with a five-dimension Chinese rubric and returns production decisions for immediate production, later production, or discard.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shiyan521](https://clawhub.ai/user/shiyan521)

### License/Terms of Use:

MIT

## Use Case:

External creators, talking-head video makers, and content operators use this skill to triage incoming clips, call excerpts, user quotes, and draft ideas with hard filters, weighted scoring, angle selection, and A/B/C production recommendations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Private or unpublished third-party information could be exposed if users copy raw material into cloud-based candidate tables.

Mitigation: Review material for privacy and unpublished third-party details before sharing; keep records local, anonymize sensitive details, or get explicit confirmation before cloud upload.

Risk: A misconfigured speaker or topic filter could admit material the creator does not intend to produce.

Mitigation: Review and tune the speaker_filter and topic_filter settings before scoring a batch, then treat filter matches as hard exclusions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/shiyan521/skills/content-material-scorer)
- [Score rubric](references/score-rubric.md)
- [Candidate table template](assets/candidate-table-template.md)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown scoring records with five dimension scores, weighted totals, A/B/C tiers, priorities, and recommended content angles.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses configurable speaker and topic filters; produces evaluation guidance and table-ready scoring fields without executing code.]

## Skill Version(s):

1.0.0 (source: release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
