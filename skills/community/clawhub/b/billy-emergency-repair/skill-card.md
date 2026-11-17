## Description:

Performs Neill-authorized emergency repair on Billy system authentication by clearing stale tokens, backing up configuration, restarting the gateway, and verifying recovery.

This skill is ready for commercial/non-commercial use.

## Publisher:

[highlander89](https://clawhub.ai/user/highlander89)

### License/Terms of Use:


## Use Case:

Neill or explicitly authorized Billy/SAPCONET maintainers use this skill during authentication or gateway emergencies to run a controlled repair workflow, verify recovery, and collect logs for follow-up.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks an agent to run unbundled local scripts that use SSH keys to change authentication state on a remote Billy system.

Mitigation: Install and run only in the Billy/SAPCONET environment after independent review of the repair and SSH key setup scripts.

Risk: Unauthorized or stale requests could trigger disruptive emergency repair actions.

Mitigation: Require explicit, current Neill authorization before execution and reject use by anyone else.

## Reference(s):

- [ClawHub skill release page](https://clawhub.ai/highlander89/skills/billy-emergency-repair)

## Skill Output:

**Output Type(s):** [Shell commands, Guidance, Markdown, Configuration]

**Output Format:** [Markdown with inline bash code blocks and troubleshooting guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces repair instructions and expected log artifacts for a Neill-authorized Billy authentication recovery workflow.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
