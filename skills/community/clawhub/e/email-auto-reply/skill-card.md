## Description:

Email Auto Reply helps users manage and test local keyword-based reply templates from a Chinese-language command-line interface.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sxliuyu](https://clawhub.ai/user/sxliuyu)

### License/Terms of Use:

MIT-0

## Use Case:

Customer support staff, busy individuals, and workflow operators can use this skill to create, list, delete, and test keyword-based email reply templates locally before reusing the response text elsewhere.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Users may assume the skill sends email, manages multiple accounts, or performs automatic CC because those capabilities are claimed in the skill description.

Mitigation: Treat it as a local reply-template manager only; verify email delivery, account handling, and CC workflows with separate tooling before operational use.

Risk: Reply rules and message templates are stored in a local file under the user's home directory.

Mitigation: Avoid storing secrets or sensitive customer data in templates and apply local file access controls appropriate for the environment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/sxliuyu/skills/email-auto-reply)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Command-line text output and JSON rule storage]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Stores reply rules locally in ~/.email_auto_reply.json.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
