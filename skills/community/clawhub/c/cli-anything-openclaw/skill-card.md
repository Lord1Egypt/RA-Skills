## Description:

Adapts HKUDS CLI-Anything for OpenClaw workflows that build, refine, test, or validate agent-native CLI harnesses for GUI applications or source repositories.

This skill is ready for commercial/non-commercial use.

## Publisher:

[barrontang](https://clawhub.ai/user/barrontang)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to analyze software projects, design agent-friendly command groups and state models, build or refine CLI-Anything harnesses, and validate packaging, tests, and JSON-oriented command behavior.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may guide an agent to create or modify project files, especially under an agent-harness directory.

Mitigation: Run it in a controlled workspace, review proposed changes and diffs, and keep unrelated work separate before applying generated harness files.

Risk: The workflow may clone repositories, install editable Python packages, run tests, and invoke local GUI or backend software through subprocesses.

Mitigation: Use trusted source paths or repository URLs, review commands before execution, and run validation in an environment where local installs and subprocess side effects are acceptable.

Risk: Generated harness plans or validation findings can be incomplete or incorrect for a target application's real backend behavior.

Mitigation: Require real backend E2E tests, inspect produced artifacts, and verify documented limitations before relying on a generated harness.

## Reference(s):

- [Agent Harness: GUI-to-CLI for Open Source Software](references/harness.md)
- [CLI-Anything for Codex](references/codex-skill.md)
- [cli-anything Command](references/cli-anything.md)
- [cli-anything-refine Command](references/cli-anything-refine.md)
- [cli-anything-validate Command](references/cli-anything-validate.md)
- [cli-anything-test Command](references/cli-anything-test.md)
- [cli-anything-list Command](references/cli-anything-list.md)
- [ClawHub skill page](https://clawhub.ai/barrontang/skills/cli-anything-openclaw)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with code snippets, shell commands, file paths, and validation summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose or create an agent-harness directory, CLI package files, tests, documentation, and JSON-capable command behavior when the user asks the agent to implement a harness.]

## Skill Version(s):

0.1.0 (source: evidence.json release.version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
