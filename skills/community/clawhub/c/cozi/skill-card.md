## Description:

Interact with Cozi Family Organizer (shopping lists, todo lists, item management). Unofficial API client for family organization.

This skill is ready for commercial/non-commercial use.

## Publisher:

[angusthefuzz](https://clawhub.ai/user/angusthefuzz)

### License/Terms of Use:


## Use Case:

External users and family organizers can use this skill to have an agent run Cozi list and calendar commands for viewing, creating, updating, and deleting household items and appointments.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles raw Cozi credentials and caches bearer tokens in a local session file.

Mitigation: Use a dedicated Cozi account when possible, inject credentials through the environment, restrict permissions on .env and .session.json files, and remove cached sessions when they are no longer needed.

Risk: Commands can delete Cozi lists or remove calendar appointments without documented confirmation or undo behavior.

Mitigation: Review the exact command and identifiers before execution, and prefer read-only commands when the requested task does not require mutation.

Risk: The skill uses an unofficial reverse-engineered Cozi API that may change without notice.

Mitigation: Validate behavior in a low-impact account before relying on it for important household lists or appointments.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/angusthefuzz/skills/cozi)
- [Cozi REST API base URL](https://rest.cozi.com/api/ext/2207)
- [cozi-api-client reference](https://github.com/BrandCast-Signage/cozi-api-client)
- [py-cozi reference](https://github.com/Wetzel402/py-cozi)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Plain text CLI output and Markdown command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js and Cozi credentials; some commands mutate Cozi lists and calendar entries.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
