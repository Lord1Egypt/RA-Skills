## Description:

ClawVet scans third-party AI agent skills, rules, hooks, and MCP configs, then uses its A-to-F grade to guide installation and trust decisions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mohibshaikh](https://clawhub.ai/user/mohibshaikh)

### License/Terms of Use:

MIT

## Use Case:

Agent developers and administrators use ClawVet to review third-party skills and related configuration before installation. They can also audit installed tools and check updates for newly introduced permissions or risks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security evidence flags unpinned npx references, which can run a package version that changes over time.

Mitigation: Review the referenced commands and use a pinned version or an already installed, trusted ClawVet release before running them.

Risk: The scan was partial because several local references could not be resolved, leaving some behavior outside the scanner's coverage.

Mitigation: Resolve the missing references and rerun a complete local scan before relying on its verdict.

## Reference(s):

- [ClawVet project repository](https://github.com/MohibShaikh/clawvet)
- [ClawVet on ClawHub](https://clawhub.ai/mohibshaikh/skills/clawvet)

## Skill Output:

**Output Type(s):** [Analysis, Guidance, Shell commands, Configuration instructions]

**Output Format:** [Markdown with findings, shell commands, and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include a scan grade, findings, capability summaries, and remediation guidance.]

## Skill Version(s):

0.16.2 (source: server-resolved release metadata; artifact frontmatter lists 0.18.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
