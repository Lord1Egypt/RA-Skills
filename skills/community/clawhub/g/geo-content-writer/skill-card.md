## Description:

GEO Content Writer turns Dageno GEO prompt opportunities into a real-fanout backlog, then produces an editorial brief, draft and review contracts, a publish-ready article, and optional WordPress handoff.

This skill is ready for commercial/non-commercial use.

## Publisher:

[geo-seo](https://clawhub.ai/user/geo-seo)

### License/Terms of Use:

MIT-0

## Use Case:

External GEO, SEO, agency, and content operations teams use this skill to convert Dageno opportunity data into a prioritized fanout backlog and one publish-ready article package from a selected backlog row.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can publish generated content to WordPress.

Mitigation: Keep WordPress status at draft unless a human explicitly approves publication, and review generated articles before publishing.

Risk: Credential destination controls are weak for Dageno and WordPress integrations.

Mitigation: Use least-privilege Dageno and WordPress credentials, install only when the publisher is trusted, and use HTTPS-only trusted site URLs.

Risk: Citation-page crawling can fetch external pages during article preparation.

Mitigation: Run citation crawling in a network-restricted environment when possible and avoid custom Dageno base URLs outside controlled testing.

Risk: Generated article examples show possible quality and topic-consistency issues.

Mitigation: Run the article quality gate and require human editorial review before publication.

## Reference(s):

- [GEO Content Writer ClawHub page](https://clawhub.ai/geo-seo/skills/geo-content-writer)
- [GEO Content Writer repository homepage](https://github.com/GEO-SEO/geo-content-writer)
- [Dageno](https://dageno.ai/?utm_source=github&utm_medium=social&utm_campaign=official)
- [Pipeline Spec](references/pipeline-spec.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown, JSON payloads, and shell command guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces fanout backlog JSON, publish-ready payload JSON, decision-grade Markdown articles, quality-gate results, and optional WordPress draft or publish handoff.]

## Skill Version(s):

0.7.3 (source: frontmatter, pyproject.toml, manifest.json, server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
