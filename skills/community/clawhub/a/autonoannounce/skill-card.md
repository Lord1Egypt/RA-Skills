## Description:

Build, operate, and troubleshoot Autonoannounce local speaker text-to-speech using the queued pipeline (enqueue to worker to ElevenLabs to playback backend).

This skill is ready for commercial/non-commercial use.

## Publisher:

[ironystock](https://clawhub.ai/user/ironystock)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to configure, benchmark, and troubleshoot low-latency local speaker text-to-speech flows backed by ElevenLabs synthesis and local playback tools. It supports queue health checks, first-run setup, backend validation, earcon management, and latency tuning.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses an ElevenLabs API key and sends synthesis or preflight requests to ElevenLabs.

Mitigation: Install only in trusted workspaces, provide a scoped credential where possible, and confirm that outbound ElevenLabs requests are acceptable for the intended text content.

Risk: Local playback backends and PowerShell invocation paths can introduce command-execution risk if filenames or backend choices are not constrained.

Mitigation: Restrict playback backends to an explicit allowlist and pass audio filenames as data rather than executable shell text.

Risk: The skill writes local config, queue, log, and earcon state under config/, .openclaw/, and audio/earcons/.

Mitigation: Constrain writable state to the skill workspace, review generated files before routine use, and avoid shared or sensitive output paths.

Risk: Fixed temporary response files can expose avoidable local file handling risk.

Mitigation: Use private temporary files for API responses and remove stale temporary data after diagnostics complete.

## Reference(s):

- [Autonoannounce ClawHub Page](https://clawhub.ai/ironystock/skills/autonoannounce)
- [Publisher Profile](https://clawhub.ai/user/ironystock)
- [Autonoannounce Homepage](https://github.com/ironystock/autonoannounce)
- [Runbook](references/runbook.md)
- [Config Contract](references/config-contract.md)
- [Performance SLOs](references/perf-slos.md)
- [Foreground Path Optimization](references/front-path-optimization.md)
- [Earcon Library](references/earcon-library.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands, JSON configuration examples, and diagnostic results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce local setup commands, queue diagnostics, playback validation steps, and benchmark summaries.]

## Skill Version(s):

0.2.5 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
