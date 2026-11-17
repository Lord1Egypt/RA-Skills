## Description:

Aero coordinates AEO monitoring workflows across canonry data, aeo-audit analysis, persistent user-scoped memory, reporting, and regression response.

This skill is ready for commercial/non-commercial use.

## Publisher:

[arberx](https://clawhub.ai/user/arberx)

### License/Terms of Use:

MIT-0

## Use Case:

Operators, developers, and AEO analysts use Aero to monitor AI answer-engine mention and citation coverage, investigate regressions, expand tracked-query baskets, and produce client-facing recommendations grounded in canonry evidence.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: WordPress and Elementor workflows can affect production pages and site structure.

Mitigation: Use staging first, keep backups, verify visual changes across viewports, and require explicit human approval before production edit or delete actions.

Risk: MCP authentication guidance involves WordPress application credentials.

Mitigation: Keep credentials out of committed project files and use separate least-privilege accounts for staging and production.

Risk: The orchestration playbook invokes a mutable npx package for aeo-audit.

Mitigation: Pin or preinstall the audit tool before using it in controlled environments.

Risk: Durable memory can retain client or project facts beyond the current session.

Mitigation: Store only user-scoped preferences or validated notes; read project state from canonry instead of persisting it in agent memory.

## Reference(s):

- [Aero on ClawHub](https://clawhub.ai/arberx/skills/aero)
- [Canonry](https://canonry.ai)
- [AEO Discovery](references/aeo-discovery.md)
- [Memory Patterns](references/memory-patterns.md)
- [Orchestration Workflows](references/orchestration.md)
- [Regression Playbook](references/regression-playbook.md)
- [Reporting Templates](references/reporting.md)
- [Elementor and WordPress MCP Development Guide](references/wordpress-elementor-mcp.md)
- [WordPress MCP Adapter](https://github.com/WordPress/mcp-adapter)
- [Elementor MCP](https://github.com/msrbuilds/elementor-mcp)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands, JSON snippets, reports, and code or content diffs when approved.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose operational writes, audits, report generation, and WordPress or Elementor changes; user approval is expected before quota-consuming or production-impacting actions.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
