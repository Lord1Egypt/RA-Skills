## Description: <br>
Behavioural intelligence layer for OpenClaw agents that monitors live decisions, requires transparent financial reasoning before purchases, detects SOUL identity drift, maps combinatorial risk across skill sets, investigates incidents, tracks memory integrity, manages multi-agent trust chains, provides emergency shutdown, and actively improves the agent setup. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cognitae-ai](https://clawhub.ai/user/cognitae-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
OpenClaw users and agent operators use Blacklight to add behavioral monitoring, financial decision review, memory-integrity checks, incident investigation, and governance reporting around an active agent session. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Blacklight asks to inspect and profile a broad range of sensitive agent activity, including memories, messaging channels, scheduled tasks, model configuration, credentials-adjacent context, and financial activity. <br>
Mitigation: Before enabling it, define exactly which sources it may inspect and where logs and cross-session profiles are stored, retained, and deleted. <br>
Risk: Audit exports, skill rewrites, hardening changes, learned auto-approvals, and autonomous modes can affect governance boundaries or disclose sensitive session context. <br>
Mitigation: Require explicit user review for those operations and keep autonomous behavior disabled unless the operator has approved the scope. <br>


## Reference(s): <br>
- [BlackLight homepage](https://github.com/cognitae-ai/BlackLight) <br>
- [BLACKLIGHT-SPEC.md](artifact/BLACKLIGHT-SPEC.md) <br>
- [taxonomy.md](artifact/taxonomy.md) <br>
- [audit-format.md](artifact/audit-format.md) <br>
- [financial.md](artifact/financial.md) <br>
- [setup-ingestion.md](artifact/setup-ingestion.md) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Markdown, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown reports, structured audit entries, and configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include risk ratings, action classifications, incident summaries, financial reasoning blocks, and governance reports.] <br>

## Skill Version(s): <br>
0.1.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
