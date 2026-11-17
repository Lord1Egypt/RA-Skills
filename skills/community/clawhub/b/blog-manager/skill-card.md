## Description:

Manage Blog System API v1.0.0 through CLI subcommands for articles, labels, users, comments, messages, moods, uploads, and health checks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yangaiwu](https://clawhub.ai/user/yangaiwu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to manage a Blog System API instance from an agent-driven CLI workflow, including content, users, comments, messages, uploads, and health checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can create, upload, update, and delete live blog content on the configured API instance.

Mitigation: Use it only against a blog instance you control, preferably a private admin or test endpoint, and confirm delete and upload targets before execution.

Risk: The target API is described as unauthenticated and does not require secure transport.

Mitigation: Prefer HTTPS, restrict access to trusted networks, and avoid passing real passwords with --pwd unless the deployment has appropriate controls.

## Reference(s):

- [API Endpoint Reference](artifact/references/api-reference.md)
- [Test Command Variables](artifact/templates/test-vars.json)
- [ClawHub Skill Page](https://clawhub.ai/yangaiwu/skills/blog-manager)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown and JSON-oriented CLI results with shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires BLOG_MANAGER_BASE_URL to point to the target Blog System API.]

## Skill Version(s):

2.1.2 (source: server release evidence; artifact frontmatter declares 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
