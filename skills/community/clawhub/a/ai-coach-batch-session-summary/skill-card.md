## Description:

Batch-analyzes ASR recording transcripts and generates a multidimensional outreach insight report.

This skill is ready for commercial/non-commercial use.

## Publisher:

[legionspace-hackathon](https://clawhub.ai/user/legionspace-hackathon)

### License/Terms of Use:

MIT-0

## Use Case:

Sales and operations teams use this skill to turn batches of completed ASR recordings into outreach-dimension statistics, charts, excerpts, and a shareable HTML report.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Recording transcripts can contain private or identifying information and may be exposed through shareable report links.

Mitigation: Use private or expiring authenticated report delivery and redact identifiers and raw excerpts by default before approval.

Risk: Bundled live-looking test artifacts may disclose transcript content or operational details.

Mitigation: Remove live transcript test artifacts from the release package or replace them with minimal synthetic fixtures.

Risk: Custom dimensions and upload destinations can change what content is extracted and where reports are delivered.

Mitigation: Validate custom dimension files and approved upload destinations before execution.

Risk: Report rendering depends on external browser scripts.

Mitigation: Bundle report scripts locally or pin external script integrity where supported.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/legionspace-hackathon/skills/ai-coach-batch-session-summary)
- [DIMENSIONS.md](artifact/DIMENSIONS.md)
- [ASR insight template](artifact/asr_insight_template.html)

## Skill Output:

**Output Type(s):** [Markdown, HTML, Shell commands, JSON, Guidance]

**Output Format:** [Markdown response with a shareable HTML report link and optional JSON metadata]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generates report files only when ASR records are present; may write local temporary files before upload.]

## Skill Version(s):

1.1.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
