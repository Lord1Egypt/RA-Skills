## Description:

Provision and manage @clawemail.com Google Workspace email accounts for AI agents, including account creation, availability checks, and existing account administration.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cto1](https://clawhub.ai/user/cto1)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to provision @clawemail.com Google Workspace email accounts for agents, check prefix availability, and administer account lifecycle actions such as suspend, unsuspend, and delete.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can use CLAWEMAIL_API_KEY to administer ClawEmail accounts.

Mitigation: Install it only when ClawEmail administration is intended, scope API key access carefully, and avoid exposing the key in shared logs or prompts.

Risk: Created accounts return passwords, OAuth connect URLs, and credentials JSON that are sensitive secrets.

Mitigation: Store returned secrets securely immediately and avoid pasting them into public or untrusted contexts.

Risk: Account deletion is destructive and can remove the Google Workspace account and associated data.

Mitigation: Require explicit confirmation before running delete actions and prefer suspend or unsuspend when reversible administration is sufficient.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/cto1/skills/claw-admin)
- [ClawHub publisher profile](https://clawhub.ai/user/cto1)
- [ClawEmail service](https://clawemail.com)
- [ClawEmail admin API](https://clawemail.com/api/emails)
- [ClawEmail self-service signup](https://clawemail.com/signup?prefix=DESIRED_PREFIX)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration instructions, API calls, JSON, Guidance]

**Output Format:** [Markdown with inline bash commands and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires CLAWEMAIL_API_KEY for admin endpoints; public availability checks and self-service signup do not require the API key.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
