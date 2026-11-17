## Description:

Generate or refine agent-usable CLIs for existing software/codebases using the CLI-Anything methodology.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jasonchenjc](https://clawhub.ai/user/jasonchenjc)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to assess whether CLI-Anything fits a target app or repository, inspect existing CLI-Anything harnesses, and package generated harness workflows for OpenClaw.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installing mutable local packages into a shared Python environment or PATH can affect other projects and make later behavior harder to reproduce.

Mitigation: Review the local CLI-Anything checkout and harness setup files first, then use a disposable workspace or virtual environment and pin dependencies where possible.

Risk: Generated or third-party harness code may not match its stated backend behavior until inspected and tested.

Mitigation: Treat generated and third-party harness code as untrusted until reviewed, and verify real entry points and minimal backend execution before claiming a harness works.

## Reference(s):

- [CLI Anything on ClawHub](https://clawhub.ai/jasonchenjc/skills/cli-anything)
- [Bundled harnesses in CLI-Anything](references/bundled-harnesses.md)
- [Adapting CLI-Anything into OpenClaw](references/openclaw-adaptation-notes.md)
- [Validated example: gimp harness](references/validated-example-gimp.md)

## Skill Output:

**Output Type(s):** [Analysis, Guidance, Shell commands, Code, Configuration]

**Output Format:** [Markdown with inline shell commands and code-oriented guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill may direct agents to inspect local repositories, verify harness prerequisites, and produce or refine OpenClaw-compatible workflow files.]

## Skill Version(s):

0.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
