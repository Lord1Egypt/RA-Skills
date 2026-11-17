## Description:

Systematic root-cause debugging with verification.

This skill is ready for commercial/non-commercial use.

## Publisher:

[iliaal](https://clawhub.ai/user/iliaal)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to investigate errors, stack traces, broken or flaky tests, regressions, and other unexpected behavior. It guides evidence-backed root-cause analysis and verification of authorized repairs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Diagnostic reports may expose sensitive environment or project information if shared without review.

Mitigation: Review and sanitize diagnostics for credentials, customer data, hostnames, IP addresses, paths, and SQL fragments before saving or sharing them.

Risk: The security analysis reports broad diagnostic collection and logging, and notes that one script was only partially analyzed.

Mitigation: Review the diagnostic collection and logging behavior before use, and limit collection to information needed for the investigation.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/iliaal/skills/compound-eng-debugging)
- [Baseline and data handling](references/baseline-and-data-handling.md)
- [Reproduction and investigation](references/reproduction-and-investigation.md)
- [Root-cause tracing](references/root-cause-tracing.md)
- [Competing hypotheses](references/competing-hypotheses.md)
- [Repair and escalation](references/repair-and-escalation.md)
- [Specialized debugging patterns](references/specialized-patterns.md)
- [Defense in depth](references/defense-in-depth.md)
- [Diagnostic collection script](scripts/collect-diagnostics.sh)

## Skill Output:

**Output Type(s):** [Markdown, Text, Code, Shell commands, Guidance]

**Output Format:** [Structured Markdown debugging report with evidence, findings, and repair or verification guidance; code or shell commands when relevant.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Report scope and proposed or verified changes depend on the request and available evidence.]

## Skill Version(s):

5.1.6 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
