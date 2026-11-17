## Description:

Command Runner helps an agent run a base64-encoded shell command through a Python wrapper and inspect stdout, stderr, and the exit code.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zww-v5](https://clawhub.ai/user/zww-v5)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and automation engineers use this skill when an agent needs to invoke a Python command wrapper instead of calling a shell directly. It is suited to workflows that require passing an encoded command argument and then reviewing stdout, stderr, and the process exit code.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can execute arbitrary host shell commands.

Mitigation: Install only in a tightly sandboxed environment and allow only explicit, trusted command arguments.

Risk: Encoded command arguments can obscure what will execute.

Mitigation: Decode and review the command before invocation, and treat the invocation as equivalent to running the decoded command directly in a terminal.

## Reference(s):

- [API Reference](references/api_reference.md)

## Skill Output:

**Output Type(s):** [Shell commands, Text, Code, Guidance]

**Output Format:** [Markdown with inline bash commands and command-output text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The helper script base64-encodes stdout, writes stderr as plain text, and returns the child process exit code.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
