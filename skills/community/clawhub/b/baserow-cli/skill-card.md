## Description:

Baserow: Create, read, update, and delete rows, list tables and fields.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jzakirov](https://clawhub.ai/user/jzakirov)

### License/Terms of Use:


## Use Case:

Developers and agents use this skill to inspect Baserow databases, list tables and fields, query rows, and create, update, or delete records through the baserow CLI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Delete and batch-delete commands can permanently change Baserow database records.

Mitigation: Confirm destructive requests with the user before execution and pass --yes only after that confirmation.

Risk: The skill requires Baserow credentials and can read or modify database content.

Mitigation: Use a least-privilege Baserow token, keep BASEROW_TOKEN out of logs, and prefer a reviewed, pinned baserow-cli package.

## Reference(s):

- [Baserow](https://baserow.io)
- [ClawHub skill page](https://clawhub.ai/jzakirov/skills/baserow-cli)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash commands and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Baserow CLI responses are JSON by default, with errors emitted to stderr as JSON.]

## Skill Version(s):

0.1.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
