## Description:

Guides agents through inspecting and managing AtomGit repositories, collaboration workflows, CI, organizations, and AIHub features using a preconfigured AtomGit MCP server.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kylezhang](https://clawhub.ai/user/kylezhang)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and teams use this skill to inspect or change AtomGit repositories, pull requests, issues, CI workflows, and related account or organization resources when they have an AtomGit MCP server configured.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A token with broad privileges could expose or change sensitive AtomGit resources.

Mitigation: Configure ATOMGIT_TOKEN outside chat and use the smallest scope needed for the task.

Risk: Write or destructive operations may alter repositories, CI runs, webhooks, or account and organization settings.

Mitigation: Require explicit confirmation before write, destructive, organization, enterprise, webhook, runner, or account-profile changes.

## Reference(s):

- [AtomGit skill homepage](https://atomgit.com/zkxw2008/AtomGit-Skills)
- [AtomGit MCP server](https://atomgit.com/zkxw2008/AtomGit-MCP-Server)
- [Setup and safety guidance](artifact/references/setup-and-safety.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Configuration instructions, Guidance]

**Output Format:** [Markdown and plain text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a separately configured AtomGit MCP server and ATOMGIT_TOKEN for live operations.]

## Skill Version(s):

1.1.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
