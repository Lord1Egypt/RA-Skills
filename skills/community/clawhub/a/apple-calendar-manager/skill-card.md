## Description:

Manage Apple Calendar events via AppleScript, with current scripts focused on adding events using relative or explicit dates.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cryptol0rd](https://clawhub.ai/user/cryptol0rd)

### License/Terms of Use:


## Use Case:

External users and developers on macOS use this skill to add Apple Calendar events from relative dates or explicit date/time values through agent-guided shell and AppleScript commands.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The package appears incomplete because the add_event.scpt helper referenced by the skill is not included.

Mitigation: Confirm the missing script is supplied from a trusted source before installation and test on a non-critical calendar.

Risk: Running the add-event command can create real Apple Calendar entries and may prompt macOS for Calendar automation permission.

Mitigation: Review event details before execution and authorize Calendar automation only for trusted agent workflows.

## Reference(s):


## Skill Output:

**Output Type(s):** [Shell commands, Guidance, Configuration]

**Output Format:** [Markdown with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires macOS, Apple Calendar access, and Calendar automation authorization.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
