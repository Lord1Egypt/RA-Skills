## Description:

ClawGuard Security Assistant helps OpenClaw users read scan reports, explain findings, analyze fix impact, and guide configuration remediation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[r0llcre](https://clawhub.ai/user/r0llcre)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw operators use this skill to understand ClawGuard scan reports, prioritize findings, assess remediation impact, and prepare reviewed configuration changes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Remediation guidance can lead an agent to edit configuration files or run commands from insufficiently verified report data.

Mitigation: Require explicit user confirmation, review the proposed path and diff, create a backup, and validate the report source before applying changes.

Risk: Local L2 scan workflows may send local security metadata to clawguardsecurity.ai.

Mitigation: Use L2 scans only when the user trusts the service, has inspected the generated command, and accepts the metadata sharing.

Risk: Fixes can break existing OpenClaw integrations, hooks, channels, or skill permissions.

Mitigation: Perform impact analysis first and review affected skills, hooks, allowlists, backups, and restart steps before changing configuration.

## Reference(s):

- [ClawGuard homepage](https://clawguardsecurity.ai)
- [ClawGuard skill repository](https://github.com/R0llcre/clawguard-skill)
- [OpenClaw](https://github.com/openclaw/openclaw)
- [Report parsing](references/report-parsing.md)
- [Finding explanations](references/finding-explain.md)
- [Finding catalog](references/finding-catalog.md)
- [Impact analysis](references/impact-analysis.md)
- [Fix procedures](references/fix-procedures.md)
- [Scan guide](references/scan-guide.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with tables, diff blocks, command snippets, and concise next steps]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Responds in the user's language and uses severity prefixes for findings.]

## Skill Version(s):

1.0.7 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
