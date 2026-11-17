## Description:

Multi-instance Gateway fleet management pack for status monitoring, dynamic add and remove operations, broadcast commands, configuration synchronization, and fleet inventory.

This skill is ready for commercial/non-commercial use.

## Publisher:

[romainsantoli-web](https://clawhub.ai/user/romainsantoli-web)

### License/Terms of Use:

MIT

## Use Case:

Developers and operators use this skill to monitor and coordinate multiple Gateway instances, including health checks, inventory listing, scaling, command broadcast, and configuration synchronization.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Fleet-wide add, remove, broadcast, and configuration synchronization actions could affect many Gateway instances at once if invoked with the wrong target or intent.

Mitigation: Use this skill only where fleet-wide operations are intended, and require explicit targeting, confirmation, authorization checks, validation, and rollback procedures before applying changes.

Risk: The security review flagged insufficient safety scoping and user-control guidance for broad fleet operations.

Mitigation: Review the skill carefully before installing it in a real Gateway fleet and add local operating controls that constrain who can run fleet-wide actions.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with YAML and command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires mcp-openclaw-extensions >= 3.0.0.]

## Skill Version(s):

1.0.0 (source: frontmatter and ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
