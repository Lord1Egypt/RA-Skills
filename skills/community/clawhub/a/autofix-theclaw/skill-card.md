## Description:

A comprehensive, self-evolving skill designed to diagnose and solve OpenClaw issues by following a structured, multi-stage resolution cycle with proactive prediction, robustness checks, knowledge creation, and diagnosis report visualization.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mikewongonline](https://clawhub.ai/user/mikewongonline)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to troubleshoot OpenClaw bugs, configuration failures, and implementation questions through structured triage, documentation and issue search, validation, and diagnostic reporting. It may propose shell commands, repair steps, rollback guidance, and knowledge updates after a problem is resolved.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: External search and diagnostic reporting can expose raw logs, tokens, hostnames, private paths, or project names.

Mitigation: Use only in non-sensitive workspaces and redact logs, tokens, hostnames, private paths, and project names before search, persistence, or report generation.

Risk: The skill may suggest modifying repair commands such as `openclaw doctor --fix` or commands requiring `sudo`.

Mitigation: Require explicit review and approval of each repair command, confirm the target environment, and provide a rollback command before execution.

Risk: Memory/profile access and knowledge updates may retain sensitive troubleshooting context.

Mitigation: Avoid broad memory writes for sensitive sessions and review any saved facts for credentials, private identifiers, or internal project details.

Risk: Generated diagnostic reports may persist sensitive execution output.

Mitigation: Disable or limit Canvas report persistence for sensitive workspaces, or store only redacted summaries.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mikewongonline/skills/autofix-theclaw)
- [OpenClaw documentation](https://docs.openclaw.ai)
- [Pre-check and context gathering module](docs/MODULE_01_PreCheck.md)
- [Search chain module](docs/MODULE_02_SearchChain.md)
- [Validation and action module](docs/MODULE_03_ValidationAction.md)
- [Diagnosis report and error intelligence module](docs/enhancement/MODULE_03_Enhancement_Reports.md)
- [Quick start v5.0](docs/tutorials/QUICK_START_v5.0.md)
- [Verification final report](docs/reports/VERIFICATION_FINAL.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands, JSON-like diagnostic summaries, and optional HTML diagnostic reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include risk levels, confidence scores, evidence-chain summaries, recommended fixes, rollback commands, and generated diagnostic report content.]

## Skill Version(s):

5.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
