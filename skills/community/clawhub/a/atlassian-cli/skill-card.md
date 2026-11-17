## Description:

Reference guide for using Atlassian's aCLI to operate Jira Cloud, Atlassian organization administration, and related terminal workflows with an authenticated aCLI binary.

This skill is ready for commercial/non-commercial use.

## Publisher:

[peetzweg](https://clawhub.ai/user/peetzweg)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, operators, and Atlassian administrators use this skill to draft, review, and safely execute aCLI commands for Jira work items, projects, boards, sprints, filters, dashboards, fields, user administration, authentication, and workflow automation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Authenticated aCLI commands can change or delete Jira and Atlassian organization resources, including work items, projects, custom fields, and managed users.

Mitigation: Require explicit current-turn approval for destructive or organization-wide commands, enumerate affected targets before execution, and preview bulk selectors with search or JSON output before applying changes.

Risk: API tokens and admin API keys can be exposed through commands, logs, shell history, or persisted intermediate files.

Mitigation: Use environment variables or stdin/file-based token input, avoid printing secrets, prefer OAuth for interactive use, and avoid embedding literal tokens in shell commands.

Risk: Bulk operations using JQL, filters, files, or ignore-errors behavior can affect unintended resources or leave partially applied administrative changes.

Mitigation: Display resolved targets and counts before execution, avoid unattended destructive bulk operations unless explicitly requested, and do not use --ignore-errors with admin user delete or deactivate commands.

## Reference(s):

- [Jira Work Item Commands Reference](references/jira-workitem-commands.md)
- [aCLI Commands Reference](references/other-commands.md)
- [Atlassian aCLI installation guide](https://developer.atlassian.com/cloud/acli/guides/install-acli/)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and command-review guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires an installed, authenticated aCLI binary; may reference API_TOKEN or API_KEY environment variables for non-interactive authentication.]

## Skill Version(s):

1.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
