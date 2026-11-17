## Description:

Manages a blog system API across 8 modules and 28 endpoints for articles, comments, labels, messages, moods, users, files, and admin workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yangaiwu](https://clawhub.ai/user/yangaiwu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to inspect, create, update, upload, and delete content in the target blog API, including articles, comments, labels, messages, moods, users, files, and admin batch operations. Use it only with blog API instances the operator controls or trusts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can modify, upload, and permanently delete remote blog content.

Mitigation: Require explicit user confirmation before create, update, delete, admin batch delete, or upload operations, and target only resources the user identifies.

Risk: The default target is a plaintext HTTP service with an embedded fallback base URL.

Mitigation: Prefer an HTTPS base URL controlled by the operator through BLOG_MINI_LJT_BASE_URL or project configuration before running mutable commands.

Risk: Admin workflows rely on a default admin/admin account and pass tokens or passwords through command arguments.

Mitigation: Rotate or disable the default admin account on the target service, avoid real secrets in command lines, and treat returned admin tokens as sensitive.

Risk: Upload commands can send local files to the remote API.

Mitigation: Restrict uploads to user-approved paths and do not let the agent choose arbitrary local files.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yangaiwu/skills/blog-mini-ljt)
- [Publisher profile](https://clawhub.ai/user/yangaiwu)
- [API endpoint reference](artifact/api-reference.md)
- [Data model schemas](artifact/schemas.md)
- [Test variables and cases](artifact/test-vars.json)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, API calls]

**Output Format:** [JSON API responses by default, with optional Markdown tables and issue-comment summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can produce remote content changes, uploaded files, deletion requests, and admin token workflows through the target blog API.]

## Skill Version(s):

1.0.0 (source: SKILL.md frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
