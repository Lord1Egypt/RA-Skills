## Description:

Concatenate and display file contents to standard output.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dinghaibin](https://clawhub.ai/user/dinghaibin)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and other agent users can use this skill to read one or more requested files and display their contents as plain text.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The helper can print any file path that the user asks it to read.

Mitigation: Review requested paths before execution and avoid using it on sensitive files unless disclosure is intended.

Risk: The documented -n and -s options are not implemented in the included script.

Mitigation: Verify expected command behavior before relying on line numbering or blank-line squeezing in a workflow.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [Plain text output with optional Markdown command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [No hidden network, persistence, or privilege behavior was reported by the authoritative security evidence.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
