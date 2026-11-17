## Description:

Blog API management tool for 26 public endpoints across articles, labels, users, comments, messages, moods, file uploads, and health checks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yangaiwu](https://clawhub.ai/user/yangaiwu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to query and manage a specific public blog API, including content creation, updates, deletion, file upload, and health checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can create, update, delete, and upload blog content through a public API.

Mitigation: Install only for trusted target blog APIs, confirm destructive actions with the user, and prefer soft deletion when available.

Risk: Local file upload commands can send user-selected files to the target API.

Mitigation: Restrict upload paths manually and review selected files before running upload commands.

Risk: Passing passwords on the command line may expose sensitive values through shell history or process listings.

Mitigation: Avoid using the --pwd argument on the command line.

Risk: The configured target API may be reached over plaintext HTTP.

Mitigation: Prefer HTTPS base URLs when the target service supports them.

Risk: Issue or PR comment behavior can post operation results to an external collaboration channel.

Mitigation: Enable that posting behavior only when the external channel is explicitly intended.

## Reference(s):

- [API Endpoint Documentation](api-reference.md)
- [Test Cases](test-vars.json)
- [ClawHub Skill Page](https://clawhub.ai/yangaiwu/skills/blog-mini-kit-ljt2)

## Skill Output:

**Output Type(s):** [API Calls, Shell commands, Markdown, JSON, Guidance]

**Output Format:** [JSON by default, with optional Markdown tables and issue comment summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses a configured BLOG_MINI_KIT_LJT2_BASE_URL and 30-second request timeouts.]

## Skill Version(s):

0.1.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
