## Description: <br>
GEO Content Writer turns Dageno prompt opportunities into a real-fanout backlog, editorial brief, draft and review contracts, and publish-ready GEO content. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[geo-seo](https://clawhub.ai/user/geo-seo) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
GEO, SEO, agency, and brand content teams use this skill to convert Dageno opportunity data into a prioritized content backlog and one publish-ready article package at a time. Developers and agent operators can also use its CLI workflow to generate backlog JSON, editorial payloads, markdown drafts, quality-gate reports, and optional WordPress handoff. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Optional WordPress commands can create, update, or publish live site content, including batch posts. <br>
Mitigation: Use a least-privilege WordPress application password, run against a staging site first, keep status set to draft until human review, and avoid exposing WordPress credentials in drafting-only sessions. <br>
Risk: Generated articles may move from draft to public content through the optional publishing workflow. <br>
Mitigation: Require editorial review and quality-gate checks before publishing, and test batch publishing behavior before using it on a production site. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/geo-seo/geo-content-writer) <br>
- [Publisher profile](https://clawhub.ai/user/geo-seo) <br>
- [Project homepage](https://github.com/GEO-SEO/geo-content-writer) <br>
- [Dageno](https://dageno.ai/?utm_source=github&utm_medium=social&utm_campaign=official) <br>
- [Pipeline spec](references/pipeline-spec.md) <br>
- [Article generation payload schema](schemas/article_generation_payload_schema.json) <br>
- [Output schema](schemas/output_schema.json) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [JSON backlog and payload files, Markdown articles, CLI command guidance, and optional WordPress post handoff.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can create local backlog and article files; optional WordPress commands can create, update, or publish remote posts when credentials and status options are provided.] <br>

## Skill Version(s): <br>
0.7.3 (source: server release metadata, skill metadata, and pyproject.toml) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
