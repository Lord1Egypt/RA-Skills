## Description:

Control cmux terminal multiplexer via its Unix socket API for workspace, surface, input, notification, sidebar metadata, and system-state operations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cnwangjie](https://clawhub.ai/user/cnwangjie)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to let an agent inspect and control a local cmux terminal multiplexer session through CLI commands or JSON-RPC over a Unix socket.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can type into terminals, press keys, split panes, or close active cmux workspaces.

Mitigation: Prefer read-only status and listing commands unless mutation is intended, and verify the target workspace or surface before mutating actions.

Risk: The skill depends on a local cmux CLI or Unix socket and may fail when that interface is unavailable.

Mitigation: Check for the cmux socket or CLI before use and handle unavailable-socket responses without retrying destructive actions.

## Reference(s):


## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Code, Configuration, API Calls]

**Output Format:** [Markdown with inline bash, JSON, and Python examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a local cmux CLI or Unix socket, normally /tmp/cmux.sock.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
