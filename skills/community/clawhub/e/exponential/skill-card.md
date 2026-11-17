## Description:

Manage tasks, projects, and workspaces in Exponential via the `exponential` CLI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[positonic](https://clawhub.ai/user/positonic)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to have an agent prepare and run Exponential CLI commands for creating, listing, triaging, and updating tasks, projects, workspaces, and kanban boards.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installing a mutable global CLI package can expose the user to unexpected package changes or untrusted code.

Mitigation: Install only if the `exponential-cli` npm package and Exponential service are trusted, and prefer a pinned or otherwise verified CLI version.

Risk: JWT authentication tokens can be exposed through pasted shell commands or shared agent logs.

Mitigation: Avoid placing real JWTs in shared prompts, shell history, or logs; rotate any token that may already have been exposed.

Risk: Create and update commands can make unintended remote changes to Exponential workspace tasks.

Mitigation: Confirm the target workspace, project, action ID, and requested change before allowing the agent to create or update tasks.

## Reference(s):

- [Exponential](https://www.exponential.im)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, JSON]

**Output Format:** [Markdown guidance with inline shell commands and JSON output examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Interactive CLI output may be pretty-printed; piped or scripted output may be JSON.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
