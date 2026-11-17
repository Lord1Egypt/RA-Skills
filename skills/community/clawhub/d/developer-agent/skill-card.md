## Description:

Orchestrates software development by coordinating with Cursor Agent, managing git workflows, and ensuring quality delivery.

This skill is ready for commercial/non-commercial use.

## Publisher:

[47vigen](https://clawhub.ai/user/47vigen)

### License/Terms of Use:


## Use Case:

Developers and engineering agents use this skill to manage implementation work from requirement analysis through git branching, optional Cursor-assisted planning or implementation, build verification, staging merge, pipeline monitoring, and final reporting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill directs agents to send all user-provided links and attachments to Cursor, which can expose sensitive information if users include secrets, customer data, private URLs, or credentials.

Mitigation: Review links and attachments before forwarding them, and do not provide secrets, private URLs, customer data, credentials, or broad attachments unless they are approved for Cursor.

Risk: The skill includes git push, staging merge, and deployment pipeline actions, which can publish unwanted changes if performed without strong review gates.

Mitigation: Require a staged diff, explicit file list, secret scan, and separate approval before any commit, push, merge, or deployment-triggering action.

Risk: The server security verdict is suspicious because the workflow gives agents broad repository and deployment authority with too little safety gating.

Mitigation: Install only in repositories where the agent is allowed to push and merge to staging, and keep human approval boundaries around source changes and deployments.

## Reference(s):

- [Developer Agent Skill Page](https://clawhub.ai/47vigen/skills/developer-agent)
- [Workflow Details](artifact/references/workflow-details.md)
- [Model Selection Matrix](artifact/references/model-selection.md)
- [Cursor Interaction Guidelines](artifact/references/cursor-guidelines.md)
- [Final Report Template](artifact/references/report-template.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and structured task reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include implementation plans, changed-file summaries, branch status, build results, deployment status, and final release notes.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
