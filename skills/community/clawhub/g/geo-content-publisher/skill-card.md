## Description:

End-to-end GEO content publishing and distribution orchestrator for turning optimized content into multi-channel publishing plans, channel-specific variants, and AI/crawler visibility packages.

This skill is ready for commercial/non-commercial use.

## Publisher:

[geolyai](https://clawhub.ai/user/geolyai)

### License/Terms of Use:

MIT-0

## Use Case:

Content, marketing, growth, and developer documentation teams use this skill to package GEO-optimized source content into launch-ready publishing briefs, channel plans, page structures, schema recommendations, AI crawler signaling steps, and final rollout timelines.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad trigger wording may cause the skill to be selected for adjacent content tasks in workspaces with many GEO or marketing skills.

Mitigation: Review whether the user is asking for end-to-end GEO publishing and distribution before applying the full workflow.

Risk: Generated publishing guidance can introduce inaccurate claims, weak citations, or unsuitable channel recommendations if the source content is incomplete.

Mitigation: Have a subject-matter owner review factual claims, canonical URLs, structured data fields, and channel copy before publishing.

Risk: The helper scripts can write Markdown output to a user-provided path.

Mitigation: Confirm output paths before running helper scripts and avoid writing into sensitive or unrelated project locations.

## Reference(s):

- [GEO Content Publisher Reference Templates](artifact/references/publishing-templates.md)
- [Geo Content Publisher on ClawHub](https://clawhub.ai/geolyai/skills/geo-content-publisher)
- [GEOlyAI Publisher Profile](https://clawhub.ai/user/geolyai)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown plans with tables, checklists, draft copy, JSON-LD snippets, and optional generated Markdown files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May coordinate conceptually with related GEO skills when present; helper scripts can generate channel-plan tables and page-structure snippets.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
