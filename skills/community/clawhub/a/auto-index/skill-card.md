## Description:

Submits URLs to the Google Indexing API in sitemap-diff or immediate URL submission modes using a Google Cloud service account with Search Console ownership.

This skill is ready for commercial/non-commercial use.

## Publisher:

[geoly-geo](https://clawhub.ai/user/geoly-geo)

### License/Terms of Use:

MIT

## Use Case:

External site owners, SEO operators, and developers use this skill to submit new or changed site URLs to Google through the Indexing API, either from a sitemap diff or from explicit URL inputs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill fetches sitemap URLs supplied at runtime.

Mitigation: Use only trusted public HTTPS sitemaps and add URL or domain allowlisting before automated use.

Risk: The skill uses Google service account credentials to publish indexing notifications.

Mitigation: Use a service account limited to the intended Search Console property and keep the key path outside shared logs or prompts.

Risk: Dependencies are installed through uv inline script metadata and may change over time.

Mitigation: Run in a constrained environment and pin or review dependencies before deployment.

## Reference(s):

- [Google Indexing API Quickstart](https://developers.google.com/search/apis/indexing-api/v3/quickstart)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, JSON]

**Output Format:** [Markdown guidance with bash commands; command execution returns structured JSON.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires uv, Python 3.10+, a Google Cloud service account key, and Search Console ownership; local sitemap cache is stored under ~/.cache/auto-index/.]

## Skill Version(s):

1.0.0 (source: SKILL.md frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
