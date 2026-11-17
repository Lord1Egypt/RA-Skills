## Description:

Generate individual Markdown articles from SerpAPI Google search results with images.

This skill is ready for commercial/non-commercial use.

## Publisher:

[near2sea](https://clawhub.ai/user/near2sea)

### License/Terms of Use:

MIT

## Use Case:

Developers and content operators can use this skill to turn SerpAPI Google search results for a keyword into dated Markdown article files with optional cover images and source links.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The bundled script includes unsafe credential handling for SerpAPI access.

Mitigation: Remove and rotate embedded secrets before use, and require the API key to come from a user-managed secret or environment variable.

Risk: The script writes output using hard-coded local paths and expects a fixed SerpAPI script location.

Mitigation: Make dependency and output paths configurable, workspace-local, and reviewed before execution.

Risk: Search keyword and result-count inputs are interpolated into generated script content.

Mitigation: Pass inputs to Python as data, validate the result count, and avoid code-generation patterns for user-provided values.

Risk: The skill downloads images from search results into the workspace.

Mitigation: Restrict permitted download schemes and hosts where appropriate, enforce file size limits, and handle failures without trusting downloaded content.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/near2sea/skills/generate-news-article)

## Skill Output:

**Output Type(s):** [Markdown, Files, Shell commands, Configuration]

**Output Format:** [Markdown files with YAML front matter and downloaded image assets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates one article per search result in a date-based output folder; content includes title, optional cover image, snippet text, and source link.]

## Skill Version(s):

1.0.0 (source: server release metadata and _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
