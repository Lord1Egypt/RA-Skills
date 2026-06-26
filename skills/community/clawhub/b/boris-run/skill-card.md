## Description: <br>
Runs multiple independent OpenClaw tasks in parallel across AI agents with load balancing, retries, progress tracking, optional verification, and artifact management. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mukston-debug](https://clawhub.ai/user/mukston-debug) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and engineers use this skill to split independent OpenClaw tasks across multiple AI agents, monitor progress, retry failures, collect artifacts, and optionally verify the results. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The release asks users to install external code from inconsistent GitHub repository references. <br>
Mitigation: Review the external repository carefully before installing, confirm which GitHub owner is authoritative, and pin installation to a known commit in an isolated Python environment. <br>
Risk: Parallel agent runs can perform many account-changing or destructive tasks at once if task prompts are not constrained. <br>
Mitigation: Start with mock or dry-run mode, require explicit approvals for destructive tasks, and avoid parallelizing sensitive operations until the workflow is verified. <br>
Risk: The optional Web UI can expose workflow controls if bound beyond the local machine. <br>
Mitigation: Keep the Web UI bound to localhost unless a reviewed access-control and network configuration is in place. <br>
Risk: Optional cleanup and uninstall commands can remove local Boris configuration or artifacts. <br>
Mitigation: Inspect the target directories, especially ~/.boris, before running deletion commands. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/mukston-debug/boris-run) <br>
- [OpenClaw](https://openclaw.dev) <br>
- [Repository listed in SKILL.json](https://github.com/mukston-debug/boris-workflow) <br>
- [Repository listed in INSTALL.md](https://github.com/mukston/boris-workflow) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands, YAML configuration examples, and structured JSON result reports] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create workflow artifacts, progress logs, and optional verification reports.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence, SKILL.json, CHANGELOG released 2026-03-18) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
