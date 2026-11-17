## Description:

Query Gerrit accounts, changes, groups, or projects and perform actions like adding reviewers, approving, submitting, or deleting changes via the Gerrit API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[craftslab](https://clawhub.ai/user/craftslab)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and release engineers use this skill to generate explicit gerritaction CLI commands for querying Gerrit resources and applying reviewer, attention, approval, submit, or delete actions to matched changes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Change actions can approve, submit, or delete all changes matched by a Gerrit query.

Mitigation: Run a query-only check first and use narrow, explicit change queries before any approve, submit, or delete action.

Risk: The provided configuration shape includes password-style credentials.

Mitigation: Do not store real Gerrit passwords in the skill directory or version control; provide credentials through a reviewed local configuration.

Risk: The installation guidance uses an unpinned external package install.

Mitigation: Use a pinned, reviewed gerritaction package version in an isolated environment before running commands against a Gerrit server.

Risk: Plain HTTP is shown for the local example host and would be unsafe for non-local Gerrit servers.

Mitigation: Use HTTPS for non-local Gerrit servers.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/craftslab/skills/gerritaction)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON output handling]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands require a Gerrit config YAML and exactly one query selector; query results can print JSON or write a new .json file.]

## Skill Version(s):

0.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
