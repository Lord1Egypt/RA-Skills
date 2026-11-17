## Description:

Interact with Akaunting open-source accounting software via REST API for bookkeeping tasks such as listing accounts, categories, transactions, and items and creating income, expense, and item records.

This skill is ready for commercial/non-commercial use.

## Publisher:

[liekzejaws](https://clawhub.ai/user/liekzejaws)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to connect an agent to an Akaunting instance, inspect accounting records, and create bookkeeping entries through CLI-backed REST API calls.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles financial data and uses HTTP Basic Auth, which can expose credentials if sent over unencrypted HTTP.

Mitigation: Use HTTPS or localhost-only access, firewall the service, and use a dedicated low-privilege Akaunting account.

Risk: The provided Docker setup includes default admin and database passwords.

Mitigation: Change all default passwords before use and restrict access to the Akaunting service.

Risk: The Docker repair script patches application code inside the Akaunting container.

Mitigation: Review and run it only as an administrator maintenance action, and back up the application before patching.

Risk: Credential configuration can store an Akaunting email and password on disk.

Mitigation: Restrict permissions on ~/.config/akaunting/config.json or use protected environment variables.

## Reference(s):

- [Akaunting API Reference](references/api.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and optional JSON CLI output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May read credentials from environment variables or ~/.config/akaunting/config.json and may perform Akaunting REST API calls.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
