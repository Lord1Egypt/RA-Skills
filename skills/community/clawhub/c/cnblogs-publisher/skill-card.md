## Description:

Manage CNBlogs (博客园) articles via MetaWeblog API. Supports save drafts, publish, update, and delete posts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[suversal](https://clawhub.ai/user/suversal)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and content authors use this skill to manage CNBlogs articles from an agent workflow, including drafting, listing, retrieving, updating, publishing, and deleting posts through the MetaWeblog API.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release evidence reports unsafe credential handling, including bundled test credentials and hardcoded account defaults.

Mitigation: Do not use bundled test credentials; rotate any exposed token and require credentials from environment variables or a managed secret store before use.

Risk: The release evidence reports disabled HTTPS certificate verification during authenticated CNBlogs actions.

Mitigation: Restore normal TLS certificate verification before using the skill with a real CNBlogs account.

Risk: Publishing, updating, deleting, and the bundled test script can modify a live blog account.

Mitigation: Review each write action before execution, require explicit confirmation for publishing or deletion, and avoid running tests/test_all.sh against a real account.

## Reference(s):

- [CNBlogs Publisher on ClawHub](https://clawhub.ai/suversal/skills/cnblogs-publisher)
- [CNBlogs MetaWeblog settings](https://i.cnblogs.com/settings#metaweblog)
- [MetaWeblog API reference](https://www.xmlrpc.com/metaWeblogApi)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and Python script output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires CNBLOGS_BLOG_URL, CNBLOGS_USERNAME, and CNBLOGS_TOKEN; authenticated actions can create, publish, update, or delete CNBlogs posts.]

## Skill Version(s):

1.0.1 (source: server release metadata; artifact package.json reports 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
