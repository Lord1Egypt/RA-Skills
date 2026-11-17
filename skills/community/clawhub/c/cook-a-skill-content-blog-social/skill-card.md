## Description:

Auto Content is an SEO and generative engine optimization content pipeline for crypto/Web3 teams that researches keywords, builds briefs, enriches drafts with UGC, charts, and links, and produces QA scoring.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kaokray](https://clawhub.ai/user/kaokray)

### License/Terms of Use:


## Use Case:

External content and marketing teams use this skill to plan, draft, enrich, optimize, and score SEO/GEO articles for crypto and Web3 topics. It can start from a project spec plus keyword/topic, or enter mid-pipeline with an existing draft.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automatic trend searches may expose project spec details, product themes, niche terms, or competitor names to external search providers before the user explicitly requests research.

Mitigation: Disable Stage 0 auto-run behavior or require explicit approval before any external search; remove sensitive project details before running web research.

Risk: Generated article data, citations, links, and SEO/GEO scores may be incomplete, estimated, or marked for verification.

Mitigation: Require editorial review of all statistics, source links, charts, UGC-derived claims, and QA scores before publication.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/kaokray/skills/cook-a-skill-content-blog-social)
- [Artifact skill definition](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files]

**Output Format:** [Markdown with structured sections, optional code blocks, generated chart files, inline links, and QA reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a project spec and keyword or topic for full-pipeline runs; web-derived data, citations, and generated SEO/GEO scores require human review before publication.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
