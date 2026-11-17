## Description:

Empties the system Trash or Recycle Bin on macOS, Linux, or Windows using OS-specific shell commands.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lhyhy123](https://clawhub.ai/user/lhyhy123)

### License/Terms of Use:

MIT-0

## Use Case:

Users invoke this skill to have an agent empty the local system Trash or Recycle Bin across macOS, Linux, and Windows. It is intended for deliberate cleanup requests where permanent deletion is acceptable.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill permanently empties Trash or Recycle Bin without a second confirmation.

Mitigation: Install only where this irreversible action is acceptable, invoke it deliberately, and prefer a version that asks for explicit confirmation before deletion.

Risk: The skill requests broad destructive shell authority for trash-emptying commands.

Mitigation: Review commands before execution and narrow allowed tool arguments to the specific trash-emptying commands required by each operating system.

## Reference(s):


## Skill Output:

**Output Type(s):** [shell commands, guidance]

**Output Format:** [Markdown with shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands are selected according to the detected operating system.]

## Skill Version(s):

1.1.1 (source: server release metadata; artifact frontmatter reports 1.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
