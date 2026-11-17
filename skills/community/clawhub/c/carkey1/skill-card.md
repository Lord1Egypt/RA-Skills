## Description:

Queries vehicle location and status, including locks, doors, windows, air conditioning, and power state, across Linux, macOS, and Windows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lkisme](https://clawhub.ai/user/lkisme)

### License/Terms of Use:

MIT-0

## Use Case:

External users and their agents use this skill to check where a vehicle is and whether key vehicle systems such as locks, doors, windows, power, and climate state appear secure.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles vehicle tokens and live vehicle location/status data.

Mitigation: Install only on a trusted single-user machine, avoid running it with elevated privileges, and protect or remove local cache and history files when they are no longer needed.

Risk: Local cache and history files may contain credentials, physical locations, and vehicle identifiers.

Mitigation: Restrict access to ~/.carkey_cache.json and ~/.carkey_history.json or the equivalent Windows user-profile files, and delete them before sharing or decommissioning the machine.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lkisme/skills/carkey1)
- [Publisher profile](https://clawhub.ai/user/lkisme)
- [Nokee OpenAPI endpoint](https://openapi.nokeeu.com)
- [Git for Windows](https://git-scm.com/download/win)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown and terminal text with shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include vehicle identifiers, location, status fields, dependency guidance, and authentication prompts.]

## Skill Version(s):

1.1.2 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
