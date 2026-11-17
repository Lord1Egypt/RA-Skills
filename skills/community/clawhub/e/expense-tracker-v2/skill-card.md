## Description:

Tracks expenses and income with local, Notion, Google Sheet, or Supabase storage and encrypted credential configuration.

This skill is ready for commercial/non-commercial use.

## Publisher:

[codeblackhole1024](https://clawhub.ai/user/codeblackhole1024)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to record income and expenses, review recent or filtered transactions, and generate monthly spending summaries across local or configured third-party storage backends.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Financial records and backend credentials are sensitive, and the security summary flags under-disclosed or unsafe secret and data handling practices.

Mitigation: Review the skill carefully before installing and use only test or narrowly scoped Notion, Google Sheet, or Supabase credentials.

Risk: Supplying the master password with the pass command can expose secrets in terminal history, process listings, or recorded sessions.

Mitigation: Use interactive password entry when possible, and do not enter secrets while screen-sharing or recording a terminal.

Risk: Local expense records may be stored unencrypted.

Mitigation: Treat local storage as sensitive, restrict filesystem access, and avoid storing real financial data until local record handling is verified.

## Reference(s):

- [Expense Tracker v2 ClawHub listing](https://clawhub.ai/codeblackhole1024/skills/expense-tracker-v2)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration]

**Output Format:** [Markdown with inline shell commands and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May require interactive credential configuration and password input.]

## Skill Version(s):

1.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
