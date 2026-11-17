## Description:

Turn one Campus Copilot snapshot or MCP-backed current view into a plain-language what-to-do-first answer for a student.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xiaojiou176](https://clawhub.ai/user/xiaojiou176)

### License/Terms of Use:

MIT-0

## Use Case:

Students, student-support agents, and developers use this skill to turn a Campus Copilot snapshot or read-only MCP current view into one prioritized next action with supporting evidence and trust gaps.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup may execute unpinned external Campus Copilot MCP code without integrity checks.

Mitigation: Use a pinned reviewed commit or signed release, verify checksums, use a frozen lockfile, and run the MCP server with a dedicated low-privilege account or sandbox.

Risk: Snapshot-only inputs can produce stale or incomplete triage if treated as live browser truth.

Mitigation: Keep outputs explicitly snapshot-scoped, cite the Focus Queue or snapshot surface used, and include trust gaps when live state is unavailable.

## Reference(s):

- [ClawHub Current View Triage Listing](https://clawhub.ai/xiaojiou176/skills/current-view-triage)
- [Campus Copilot MCP Setup](references/INSTALL.md)
- [Campus Copilot Capability Map](references/CAPABILITIES.md)
- [Current View Input Shape](references/input-shape.md)
- [OpenHands / OpenClaw Demo Walkthrough](references/DEMO.md)
- [Campus Copilot Troubleshooting](references/TROUBLESHOOTING.md)
- [Campus Copilot Repository](https://github.com/xiaojiou176-open/campus-copilot.git)
- [Campus Copilot MCP Bundle Release Asset](https://github.com/xiaojiou176-open/campus-copilot/releases/download/v0.1.0/campus-copilot-mcp-0.1.0.mcpb)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Plain-language Markdown with top_action, why_now, evidence_used, and trust_gaps fields.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only and snapshot-scoped; it should not claim live browser or session truth from snapshot-only evidence.]

## Skill Version(s):

1.0.0 (source: server evidence and manifest.yaml)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
