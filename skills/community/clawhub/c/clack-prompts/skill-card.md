## Description:

Build interactive Node.js command-line apps with @clack/prompts, covering prompt flows, spinners, progress bars, task runners, and styled logging.

This skill is ready for commercial/non-commercial use.

## Publisher:

[openlark](https://clawhub.ai/user/openlark)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to design Node.js CLI prompt flows with @clack/prompts and apply API patterns for inputs, selections, cancellation handling, spinners, progress bars, tasks, and logs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompt flows may collect sensitive input such as passwords or API keys.

Mitigation: Use masked inputs for secrets, avoid logging sensitive values, and review generated handling for storage or transmission before use.

Risk: Generated CLI app logic may run package installs, subprocesses, or file changes.

Mitigation: Review commands, task runner steps, subprocess arguments, and filesystem paths before execution.

Risk: Prompt cancellation can leave partially completed setup work.

Mitigation: Use isCancel and onCancel guards with explicit cleanup before exiting a prompt flow.

## Reference(s):

- [@clack/prompts API Reference](references/api.md)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands]

**Output Format:** [Markdown with JavaScript and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Documentation-only guidance for building interactive Node.js command-line apps.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
