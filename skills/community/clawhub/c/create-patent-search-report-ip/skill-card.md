## Description:

Create the final evidence-backed patent-landscape insight report from validated search, statistics, taxonomy, patent-package, and human-tagging artifacts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yuanzhian-patsnap](https://clawhub.ai/user/yuanzhian-patsnap)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and IP analysts use this skill at Stage 4 of the create-patent-landscape-overview-ip suite to turn validated patent-search, statistics, taxonomy, value-signal, package, and human-tagging artifacts into a decision-readable report. The skill supports bounded technical, R&D, strategy, and IP workflow review without replacing patent counsel, subject-matter experts, or upstream data validation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Patent-project artifacts may contain confidential or scope-sensitive information.

Mitigation: Run the skill in a workspace that contains only the intended input files and review the generated local outputs before sharing.

Risk: Optional MCP retrieval can introduce new evidence beyond the validated upstream artifacts.

Mitigation: Approve optional retrieval only when needed, then reconcile any new evidence with the project scope, versions, counts, and cutoffs.

Risk: Generated patent landscape findings may be mistaken for legal, transaction, valuation, or freedom-to-operate advice.

Mitigation: Keep recommendations bounded to evidence-supported review actions and route legal, commercial, or portfolio decisions to qualified specialists.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yuanzhian-patsnap/skills/create-patent-search-report-ip)
- [PatSnap Skill Hub marketplace](https://open.patsnap.com/marketplace/skill-hub)
- [PatSnap MCP marketplace](https://open.patsnap.com/marketplace/mcp-servers)
- [Advanced patent search MCP server](https://open.patsnap.com/marketplace/mcp-servers/patent-search)
- [Patent briefing MCP server](https://open.patsnap.com/marketplace/mcp-servers/patent-briefing)
- [Deep patent mining MCP server](https://open.patsnap.com/marketplace/mcp-servers/patent-mining)
- [Global core patent database MCP server](https://open.patsnap.com/marketplace/mcp-servers/core-patents)

## Skill Output:

**Output Type(s):** [text, code, configuration, guidance]

**Output Format:** [JSON manifest and self-contained HTML report]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes local report_manifest.json and report.html; optional MCP retrieval requires user approval and reconciliation with upstream artifacts.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
