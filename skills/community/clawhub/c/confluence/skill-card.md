## Description:

Search and manage Confluence pages and spaces using confluence-cli. Read documentation, create pages, and navigate spaces.

This skill is ready for commercial/non-commercial use.

## Publisher:

[francisbrero](https://clawhub.ai/user/francisbrero)

### License/Terms of Use:


## Use Case:

Developers, documentation maintainers, and operational teams use this skill to search, read, create, update, and export Confluence pages and spaces through the confluence-cli command-line tool.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses a Confluence token and can access sensitive workspace content.

Mitigation: Use a Confluence account or token with the minimum permissions needed and keep credentials out of prompts, logs, and shared files.

Risk: Create and update commands make live changes to Confluence pages.

Mitigation: Review generated commands and target page identifiers before execution, especially for write operations.

Risk: Export commands can write potentially sensitive documentation and attachments to local disk.

Mitigation: Choose an appropriate output directory and handle exported files according to the workspace's data handling requirements.

Risk: The skill depends on the external confluence-cli npm package.

Mitigation: Install only after trusting the package source, and preferably pin a reviewed package version.

## Reference(s):

- [ClawHub Confluence skill page](https://clawhub.ai/francisbrero/skills/confluence)
- [confluence-cli project](https://github.com/pchuri/confluence-cli)
- [confluence-cli npm package](https://www.npmjs.com/package/confluence-cli)
- [Atlassian API tokens](https://id.atlassian.com/manage-profile/security/api-tokens)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration instructions, Guidance, Files]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands may read from or write to Confluence and may export page content and attachments to local disk.]

## Skill Version(s):

1.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
