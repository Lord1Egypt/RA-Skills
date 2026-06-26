## Description: <br>
Collects, structures, searches, and repurposes saved articles, social posts, webpages, and videos into a local knowledge library. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lovensky1992-wk](https://clawhub.ai/user/lovensky1992-wk) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
OpenClaw users and developers use this skill to save content from blogs, X/Twitter, webpages, and video platforms into structured collection files, maintain search indexes, and retrieve prior saved material for reuse. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can use browser sessions, API keys, and fetched private content while collecting pages or transcripts. <br>
Mitigation: Use a dedicated browser profile and only provide credentials or private pages that are appropriate for the collection workflow. <br>
Risk: The skill persistently writes fetched content, images, comments, transcripts, and metadata into local collections and may sync them into an Obsidian vault. <br>
Mitigation: Use a dedicated collection directory or vault, and review saved files before sharing, syncing, or reusing them. <br>
Risk: The documented workflow refers to helper scripts that are not included in the reviewed artifact. <br>
Mitigation: Review or supply any missing helper scripts before relying on the full post-collection, verification, or image-cache workflow. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/lovensky1992-wk/content-collector) <br>
- [Bilibili Comments](references/bilibili-comments.md) <br>
- [Content Overview Specification](references/content-overview-spec.md) <br>
- [Highlight Extraction Specification](references/highlight-extraction-spec.md) <br>
- [Image Extraction Specification](references/image-extraction-spec.md) <br>
- [Obsidian Integration](references/obsidian-integration.md) <br>
- [Schema Extraction Specification](references/schema-extraction-spec.md) <br>
- [Theme Extraction Specification](references/theme-extraction-spec.md) <br>
- [URL Routing and Site Specifications](references/url-routing-and-site-specs.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown files with YAML frontmatter, indexes, tags, transcripts, and concise agent status messages.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write collection files under collections/ and sync copies into an Obsidian vault when configured.] <br>

## Skill Version(s): <br>
2.0.1 (source: ClawHub release metadata; artifact frontmatter: 2.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
