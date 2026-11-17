## Description:

Helps parents and sleep consultants record nursery audio and observations as searchable infant sleep logs and compare crying, feeding, waking, and settling patterns across nights.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bluecolumnconsulting-lgtm](https://clawhub.ai/user/bluecolumnconsulting-lgtm)

### License/Terms of Use:

MIT-0

## Use Case:

Parents, doulas, and pediatric sleep consultants use this skill to log overnight nursery audio and observations, then review sleep and cry patterns across nights before making care decisions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Nursery recordings and infant sleep histories are sent to an external indexing service and may expose sensitive family information.

Mitigation: Get informed parent or guardian consent, minimize names and medical details, and verify retention, deletion, and access controls before uploading real recordings.

Risk: A broadly accessible audio URL could disclose private nursery recordings.

Mitigation: Use access-controlled audio URLs and share only the recordings needed for the sleep log.

## Reference(s):

- [BlueColumn API documentation](https://bluecolumn.ai/docs)
- [ClawHub skill release](https://clawhub.ai/bluecolumnconsulting-lgtm/skills/baby-sleep-memory)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown with shell command examples and sleep-log summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Per-night events and cross-night trend summaries; requires a BlueColumn API key.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
