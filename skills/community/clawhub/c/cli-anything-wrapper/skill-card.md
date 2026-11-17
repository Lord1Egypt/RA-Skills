## Description:

Wraps CLI-Anything so OpenClaw can list and invoke command-line harnesses for supported desktop, AI, media, office, and research applications.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ntaffffff](https://clawhub.ai/user/ntaffffff)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to inspect supported CLI-Anything applications and invoke their command-line harnesses from an agent workflow. It is intended for workflows such as image editing, 3D rendering, document conversion, AI tooling, media editing, diagrams, and reference management when the required local tools are installed.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The install path can clone and run setup code from a mutable third-party CLI-Anything checkout.

Mitigation: Use a manually reviewed and pinned CLI-Anything checkout instead of relying on automatic installation.

Risk: Invoked harnesses can run local applications that may modify files, application state, or external service state.

Mitigation: Run with dry-run first, review the selected application and arguments, and execute in a constrained workspace when handling important files.

Risk: Fallback execution may run another script in a harness directory when the expected cli-anything executable is absent.

Mitigation: Verify the harness directory contents and expected executable before allowing non-dry-run execution.

## Reference(s):

- [CLI-Anything Wrapper Usage Guide](references/USAGE.md)
- [CLI-Anything](https://github.com/HKUDS/CLI-Anything)
- [OpenClaw](https://openclaw.ai)
- [ClawHub Skill Page](https://clawhub.ai/ntaffffff/skills/cli-anything-wrapper)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Plain text, JSON, and shell command output from local CLI-Anything harnesses.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can list supported applications, report wrapper information, simulate execution with dry-run, install CLI-Anything, or invoke a selected local harness with user-provided arguments.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
