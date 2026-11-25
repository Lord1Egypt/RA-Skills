## Description:

Systematic root-cause debugging with verification for errors, stack traces, broken tests, flaky tests, regressions, or other unexpected behavior.

This skill is ready for commercial/non-commercial use.

## Publisher:

[iliaal](https://clawhub.ai/user/iliaal)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to investigate unexpected software behavior, identify evidence-backed root causes, and verify authorized repairs or document remaining uncertainty.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Diagnostic collection or logging may expose secrets or sensitive project or customer information, and the reported capabilities may extend beyond the stated debugging purpose.

Mitigation: Before installation, review what diagnostic data is collected or logged and whether it is screened for secrets and sensitive information before saving or sharing; assess capabilities outside the debugging purpose.

## Reference(s):

- [ia-debugging on ClawHub](https://clawhub.ai/iliaal/skills/compound-eng-debugging)
- [Baselines and diagnostic data](references/baseline-and-data-handling.md)
- [Analysis of competing hypotheses](references/competing-hypotheses.md)
- [Defense in depth](references/defense-in-depth.md)
- [Repair and escalation](references/repair-and-escalation.md)
- [Reproduction and investigation](references/reproduction-and-investigation.md)
- [Root cause tracing](references/root-cause-tracing.md)
- [Specialized debugging patterns](references/specialized-patterns.md)
- [Diagnostic collection script](scripts/collect-diagnostics.sh)

## Skill Output:

**Output Type(s):** [Analysis, Guidance, Markdown, Shell commands, Code]

**Output Format:** [Markdown diagnostic reports and guidance, with shell commands or code snippets when relevant]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Evidence-backed conclusions with stated uncertainty and verification status]

## Skill Version(s):

5.1.7 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
