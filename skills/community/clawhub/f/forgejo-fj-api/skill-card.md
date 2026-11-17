## Description:

Forgejo via fj and REST API for repos, issues, PRs, wiki, CI, and reviews.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nerasse](https://clawhub.ai/user/nerasse)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to operate self-hosted Forgejo repositories, issues, pull requests, wiki pages, releases, CI status, and code review workflows through fj, REST API calls, and local git review steps.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Authenticated write and delete operations can change or remove Forgejo repository data.

Mitigation: Use the narrowest token scopes needed and confirm destructive repository, wiki, label, milestone, merge, and workflow dispatch actions before execution.

Risk: A leaked Forgejo token can grant repository access.

Mitigation: Avoid pasting or logging tokens; provide FORGEJO_TOKEN through the runtime environment or a secret store and rotate it if exposed.

Risk: Using the wrong Forgejo instance or repository can affect unintended resources.

Mitigation: Confirm FORGEJO_URL and owner/repo before running fj commands or REST API calls, especially outside a local clone.

## Reference(s):

- [Forgejo Workflow homepage](https://github.com/nerasse/forgejo-skill)
- [Forgejo API Cheatsheet](references/api-cheatsheet.md)
- [Forgejo CI and Actions](references/ci-actions.md)
- [Forgejo Pull Request Review Workflow](references/code-review.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, API calls, Guidance]

**Output Format:** [Markdown guidance with shell commands, HTTP examples, and JSON payload snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires FORGEJO_URL, FORGEJO_TOKEN, and relevant Forgejo token scopes; uses fj, curl, jq, and git when available.]

## Skill Version(s):

0.1.1 (source: frontmatter, changelog, release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
