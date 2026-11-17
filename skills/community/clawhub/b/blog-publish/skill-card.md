## Description:

Blog Publish helps agents create, update, delete, restore, list, and upload content through a configured public blog system API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yangaiwu](https://clawhub.ai/user/yangaiwu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and content operators use this skill to publish and manage blog articles, labels, and uploaded files through curl examples or the included Python CLI against a configured blog API.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can create, update, upload, and delete content on the configured blog server.

Mitigation: Verify BLOG_PUBLISH_BASE_URL before use and review each mutable action before execution.

Risk: Hard deletion and file uploads can be irreversible or externally visible.

Mitigation: Prefer soft deletion, require explicit confirmation for --hard deletion, and validate files before upload.

Risk: The helper script reads credential-like BLOG_PUBLISH_* values even though the API is documented as unauthenticated.

Mitigation: Store only the required base URL for this skill and avoid placing BLOG_PUBLISH_* secrets in environment variables or .project-info files.

## Reference(s):

- [API Reference - Blog System API](references/api-reference.md)
- [Test Variables](templates/test-vars.json)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline shell commands, Python CLI examples, and JSON or Markdown command output.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a configured BLOG_PUBLISH_BASE_URL or project configuration; mutable operations can create, update, upload, soft-delete, or hard-delete blog content.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
