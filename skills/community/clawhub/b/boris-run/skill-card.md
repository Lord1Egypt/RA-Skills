## Description:

Boris Workflow for OpenClaw helps agents run multiple independent tasks in parallel with load balancing, retries, progress tracking, optional verification, and organized artifact output.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mukston-debug](https://clawhub.ai/user/mukston-debug)

### License/Terms of Use:

MIT

## Use Case:

Developers and agent operators use this skill to distribute independent research, analysis, coding, review, testing, or content tasks across multiple OpenClaw agents and collect structured results.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installation depends on unreviewed mutable remote code and inconsistent repository references.

Mitigation: Confirm the correct repository, review requirements, CLI, Web UI startup script, and server code, and prefer a pinned release or commit before installation.

Risk: The optional Web UI can expose workflow controls if bound beyond the local machine.

Mitigation: Run the Web UI only on localhost unless the deployment has been reviewed and protected by appropriate access controls.

Risk: Configuration and artifact cleanup commands may remove local Boris data.

Mitigation: Back up ~/.boris before running uninstall or cleanup commands.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mukston-debug/skills/boris-run)
- [Publisher profile](https://clawhub.ai/user/mukston-debug)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands, YAML configuration examples, and JSON workflow-result descriptions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce workflow artifacts, progress logs, exported YAML configuration, and optional verification reports.]

## Skill Version(s):

1.0.0 (source: server release metadata, SKILL.json, and CHANGELOG dated 2026-03-18)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
