## Description:

Ranks a user-defined PatSnap patent candidate universe with an auditable 30/30/20/20 evidence model and generates traceable HTML, JSON, and optional Word outputs for portfolio triage.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yuanzhian-patsnap](https://clawhub.ai/user/yuanzhian-patsnap)

### License/Terms of Use:

MIT-0

## Use Case:

IP analysts, counsel, R&D leaders, and portfolio teams use this skill to screen a reviewed PatSnap patent query, prioritize a documented 10-15% subset, and prepare traceable portfolio-review materials. It supports triage and review preparation, not valuation, enforceability, validity, freedom-to-operate, or investment conclusions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: PatSnap API credentials could be exposed if placed in prompts, command arguments, logs, reports, or repositories.

Mitigation: Provide credentials only through PATSNAP_API_KEY or an explicit PATSNAP_API_KEY_FILE, and review generated artifacts to confirm credentials and private paths are absent.

Risk: Optional image handling and report viewing can trigger outbound requests to remote drawing URLs.

Mitigation: Keep Word image download off unless needed, allow only validated HTTP(S) image responses, reject redirects, cap image size, and avoid opening reports with unreviewed drawing URLs in sensitive networks.

Risk: Screening scores may be mistaken for patent value, validity, enforceability, freedom to operate, or investment merit.

Mitigation: Use the results only as evidence-based portfolio triage, retain the stated limitations, and require expert human review before legal, commercial, or investment use.

Risk: Failed or missing API evidence can distort interpretation if treated as factual zero or absence.

Mitigation: Preserve available, empty, missing, error, and not_run states in checkpoints and reports, and do not conclude absence when required evidence was not successfully retrieved.

## Reference(s):

- [High-Value Patent Portfolio Screening Standard](references/screening-standard.md)
- [Reference Implementation README](scripts/README.md)
- [PatSnap Connect REST API Base](https://connect.patsnap.com)
- [PatSnap Advanced Patent Search MCP](https://open.patsnap.com/marketplace/mcp-servers/patent-search)
- [PatSnap Patent Briefing MCP](https://open.patsnap.com/marketplace/mcp-servers/patent-briefing)
- [PatSnap Global Core Patents MCP](https://open.patsnap.com/marketplace/mcp-servers/core-patents)

## Skill Output:

**Output Type(s):** [Analysis, Files, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown guidance plus generated static HTML, JSON trace files, restartable JSON checkpoints, and optional DOCX.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a human-reviewed PatSnap query and private API key; Word output and image download are optional.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
