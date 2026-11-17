## Description:

Analyze local Codex session telemetry and produce privacy-safe efficiency reports with actionable workflow recommendations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wardlu](https://clawhub.ai/user/wardlu)

### License/Terms of Use:

MIT

## Use Case:

Developers and engineers use this skill to analyze local Codex session telemetry, compare recent sessions, and produce privacy-aware efficiency reports with actionable workflow recommendations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Telemetry-derived JSON or HTML reports can reveal workflow details, project names, paths, or other local context if shared.

Mitigation: Use telemetry-only mode by default, write reports to a dedicated directory, and review generated report paths and contents before sharing outputs.

Risk: AI diagnosis may consume Codex usage and can add advisory interpretation beyond deterministic telemetry.

Mitigation: Run AI mode only when the user explicitly requests it, and treat AI output as advisory while using deterministic telemetry as the numeric source of truth.

Risk: Running the analyzer from the wrong directory can inspect unintended session data or write reports to an unexpected location.

Mitigation: Resolve the analyzer directory from an explicit user path, CODEX_DOCTOR_DIR, or the current workspace, and pass explicit cache and output directories when needed.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/wardlu/skills/codex-doctor)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and local report paths; referenced analyzer outputs may be JSON and HTML.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Defaults to telemetry-only analysis; AI diagnosis is optional and must be explicitly requested.]

## Skill Version(s):

0.1.2 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
