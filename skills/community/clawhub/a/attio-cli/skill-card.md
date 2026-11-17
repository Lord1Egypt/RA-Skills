## Description:

Command-line tool to list, get, and manage objects, records, and lists in an Attio CRM workspace via the Attio API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[froemic](https://clawhub.ai/user/froemic)

### License/Terms of Use:


## Use Case:

Developers and CRM operators use this skill to install and use attio-cli, query Attio objects, records, and lists, and generate a Markdown schema of an Attio workspace for agent context.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installing the upstream CLI without pinning may pull unreviewed changes.

Mitigation: Review the upstream CLI before installing and pin it to a known commit or release when possible.

Risk: Attio API keys and generated workspace.schema.md can expose sensitive CRM access or metadata.

Mitigation: Use a least-privileged Attio API key, keep generated schema files out of version control, and handle them as sensitive workspace data.

Risk: Create-record and add-entry examples can modify a live CRM workspace.

Mitigation: Run write examples only in a sandbox or after confirming the intended live-workspace change.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/froemic/skills/attio-cli)
- [attio-cli Repository](https://github.com/FroeMic/attio-cli)
- [Attio API v2 Base URL](https://api.attio.com/v2)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command and API examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May generate workspace.schema.md containing sensitive CRM metadata.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
