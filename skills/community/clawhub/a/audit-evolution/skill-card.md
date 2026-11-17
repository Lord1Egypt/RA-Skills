## Description:

Audit Evolution helps an agent turn each run into reusable evidence, a snapshot, an evolution card, a memory ledger entry, a minimal patch proposal, and a next-run bootstrap before any human-approved change.

This skill is ready for commercial/non-commercial use.

## Publisher:

[adragon0707](https://clawhub.ai/user/adragon0707)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill after task completion, benchmark runs, user corrections, failures, context pressure, or skill changes to produce an auditable self-improvement package. It emphasizes evidence-grounded state tracking, restrained memory capture, one minimal patch proposal, and human approval before changes or external actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installer and runtime rules can persistently steer future agent sessions through broad automatic triggers.

Mitigation: Install only where persistent agent routing is acceptable; prefer the no-agent-update path or add a narrower manual AGENTS.md rule with explicit commands.

Risk: Agent-readable run records and user feedback can influence later sessions if they contain untrusted or overly broad guidance.

Mitigation: Do not feed untrusted summaries or raw user-feedback text into the hook; review generated run records before relying on them.

Risk: Automatic audit workflows may leave unwanted local routing blocks or run records in a workspace.

Mitigation: Remove the AGENTS.md Audit Evolution block and the .audit-evolution run records if the automatic behavior is no longer wanted.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/adragon0707/skills/audit-evolution)
- [README](README.md)
- [Adapter Guide](ADAPTERS_ZH.md)
- [Install Test Checklist](INSTALL_TEST_ZH.md)
- [Closed Loop Case Example](examples/closed_loop_case_zh.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with structured text, YAML-style entries, and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill normally produces seven audit sections plus a short command menu; installer and hook scripts can also produce workspace files and run-record metadata.]

## Skill Version(s):

0.3.3 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
