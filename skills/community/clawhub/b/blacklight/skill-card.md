## Description:

Behavioural intelligence layer for OpenClaw agents that monitors live decisions, forces transparent financial reasoning before purchases, detects SOUL identity drift, maps combinatorial risk across skill sets, investigates incidents, tracks memory integrity, manages multi-agent trust chains, provides emergency shutdown, and improves the agent setup.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cognitae-ai](https://clawhub.ai/user/cognitae-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use Blacklight to add a behavioral governance layer that audits agent actions, flags autonomy, injection, exfiltration, trust, and epistemic risks, and requires structured review for financial or consequential actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad always-on profiling can expose sensitive environment, memory, permissions, and behavior data through logs or exports.

Mitigation: Limit first-run profiling to selected data sources, redact sensitive values, and define retention rules before enabling logs or exports.

Risk: Automatic trust promotion or relaxed confirmation behavior can reduce oversight for consequential or financial actions.

Mitigation: Disable automatic trust promotion and require confirmation for every financial and consequential action before use.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/cognitae-ai/skills/blacklight)
- [Blacklight Homepage](https://github.com/cognitae-ai/BlackLight)
- [Blacklight Architecture Specification](artifact/BLACKLIGHT-SPEC.md)
- [Threat Taxonomy](artifact/taxonomy.md)
- [Audit Log Format](artifact/audit-format.md)
- [Financial Intelligence Module](artifact/financial.md)
- [Setup Ingestion and Agent Profiling](artifact/setup-ingestion.md)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance, shell commands]

**Output Format:** [Markdown reports, structured audit entries, YAML configuration snippets, and inline command-style guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include risk ratings, confirmation gates, audit records, session profiles, and configuration recommendations.]

## Skill Version(s):

0.1.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
