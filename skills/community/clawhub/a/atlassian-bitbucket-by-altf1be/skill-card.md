## Description:

Atlassian Bitbucket Cloud skill for full CRUD on repositories, pull requests, pipelines, issues, snippets, workspaces, branches, deployments, and more via Bitbucket REST API 2.0 with API Token authentication.

This skill is ready for commercial/non-commercial use.

## Publisher:

[abdelkrim](https://clawhub.ai/user/abdelkrim)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to manage Bitbucket Cloud repositories, pull requests, pipelines, issues, snippets, workspaces, branches, deployments, and related administration from an agent-assisted CLI workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can perform broad administrative Bitbucket changes, including changes to permissions, keys, variables, webhooks, runners, schedules, commits, downloads, and addons.

Mitigation: Use narrowly scoped Bitbucket API tokens and review every command that changes administrative resources before execution.

Risk: Security evidence reports a verified bug that can forward Bitbucket credentials to an untrusted pagination URL.

Mitigation: Avoid admin-wide credentials and restrict use to trusted workflows until pagination URL validation is fixed.

Risk: Passing real secrets directly on the command line may expose them through local shell or process history.

Mitigation: Prefer environment variables or other secret-handling mechanisms instead of command-line secret arguments.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/abdelkrim/skills/atlassian-bitbucket-by-altf1be)
- [Publisher Profile](https://clawhub.ai/user/abdelkrim)
- [Bitbucket REST API 2.0 Documentation](https://developer.atlassian.com/cloud/bitbucket/rest/intro/)
- [Atlassian API Tokens](https://id.atlassian.com/manage-profile/security/api-tokens)
- [API Coverage](docs/API-COVERAGE.md)
- [Bitbucket Endpoint Reference](references/bitbucket-endpoints.json)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON-oriented CLI output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands require Bitbucket credentials and may call Bitbucket REST API endpoints.]

## Skill Version(s):

1.1.0 (source: server release metadata; artifact package.json reports 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
