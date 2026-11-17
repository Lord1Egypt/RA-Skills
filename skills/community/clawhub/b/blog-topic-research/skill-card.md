## Description:

Builds a blog editorial backlog from verifiable user-demand signals by mining search, forum, issue, changelog, and optional keyword-volume sources, then returns source-backed long-tail topic scaffolds.

This skill is ready for commercial/non-commercial use.

## Publisher:

[automatelab](https://clawhub.ai/user/automatelab)

### License/Terms of Use:

MIT-0

## Use Case:

Content marketers, founders, indie hackers, and developer-tool teams use this skill to research long-tail blog topics backed by citable demand signals. It helps agents produce writer-ready topic scaffolds with sources, keywords, problem summaries, fixes, version context, and question variants.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may use web research tools and optional paid DataForSEO API calls when DATA_FOR_SEO_API_BASE64 is available.

Mitigation: Run without DATA_FOR_SEO_API_BASE64 unless paid keyword enrichment is intended, and use a scoped credential when enrichment is enabled.

Risk: The security verdict is suspicious because the optional credential-backed curl behavior is broader than a content-only description suggests.

Mitigation: Review the skill before installation, confirm the DataForSEO behavior is acceptable, and rotate the credential if command logs or process telemetry could have exposed it.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/automatelab/skills/blog-topic-research)
- [Publisher profile](https://clawhub.ai/user/automatelab)
- [Project homepage](https://github.com/AutomateLab-tech/publishing-skills)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Guidance]

**Output Format:** [Markdown topic blocks with optional JSON append output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Each accepted topic includes demand signals, primary sources, keywords, problem summary, confirmed fixes, version context, and question variants.]

## Skill Version(s):

1.1.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
