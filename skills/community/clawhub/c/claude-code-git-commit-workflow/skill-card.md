## Description:

Use when the user wants a single clean commit created from current changes with safe staging, message drafting, and non-interactive git usage.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wimi321](https://clawhub.ai/user/wimi321)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill when they want an agent to inspect current repository changes, stage only relevant files, draft an appropriate commit message, and create one non-amended git commit.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The agent may accidentally stage unrelated files or secrets while preparing the commit.

Mitigation: Review the staged diff or resulting commit summary and keep staging scoped to relevant changes before accepting the commit.

## Reference(s):


## Skill Output:

**Output Type(s):** [Text, Shell commands, Guidance]

**Output Format:** [Markdown or plain text with git command summaries and a commit result]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces one non-amended commit and a concise summary of the committed changes.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
