## Description:

Generate or refine agent-usable CLIs for existing software/codebases using the CLI-Anything methodology.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lean-zhouchao](https://clawhub.ai/user/lean-zhouchao)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to assess whether CLI-Anything fits a target app or repository, work with existing agent harnesses, and package CLI-Anything workflows into OpenClaw-compatible skills.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may guide installation or execution of mutable local CLI-Anything harness code in the current or system Python environment.

Mitigation: Review the referenced checkout first, prefer a dedicated virtual environment, and avoid system-level package installation such as --break-system-packages.

Risk: Generated or bundled harness code can be incorrect, misleading, or untrusted until inspected.

Mitigation: Inspect generated code and verify CLI entry points and real backend dependencies before relying on a harness.

Risk: Publishing or packaging workflows can push derived artifacts outside the local workspace.

Mitigation: Require explicit user approval before package installation, publishing, or other external release actions.

## Reference(s):

- [Bundled harnesses in CLI-Anything](references/bundled-harnesses.md)
- [Adapting CLI-Anything into OpenClaw](references/openclaw-adaptation-notes.md)
- [Validated example: gimp harness](references/validated-example-gimp.md)
- [ClawHub skill page](https://clawhub.ai/lean-zhouchao/skills/cli-anything-zc)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration instructions]

**Output Format:** [Markdown with inline code and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May recommend inspecting or installing local CLI-Anything harness code; review generated harnesses before execution.]

## Skill Version(s):

0.1.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
