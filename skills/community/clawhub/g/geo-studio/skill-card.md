## Description:

GEO Content Studio is a GEO content orchestration skill that classifies user goals and routes work across specialized workflows for strategy, audits, content creation, optimization, technical setup, and reporting.

This skill is ready for commercial/non-commercial use.

## Publisher:

[geoly-geo](https://clawhub.ai/user/geoly-geo)

### License/Terms of Use:


## Use Case:

External marketers, content strategists, and developers use this skill as a starting point for GEO work. It helps classify a broad GEO request and coordinate the appropriate sequence of specialized skills for content, site visibility, structured data, or reporting deliverables.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated content, JSON-LD, and llms.txt outputs may be incomplete or unsuitable for direct publication.

Mitigation: Review outputs as drafts before publishing or applying them to site files.

Risk: Downstream skills selected by the orchestrator may request permissions to edit files or publish content.

Mitigation: Review each downstream skill's permissions and behavior before allowing site changes or publication.

## Reference(s):

- [Studio Workflow Paths](artifact/references/workflow-paths.md)
- [GEO Content Studio ClawHub Listing](https://clawhub.ai/geoly-geo/skills/geo-studio)
- [GEOLY AI Publisher Profile](https://clawhub.ai/user/geoly-geo)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with workflow summaries, deliverables, schema or configuration snippets, and one recommended next step]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Routes broad GEO tasks to specialized skills and treats generated articles, JSON-LD, and llms.txt outputs as drafts for review.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
