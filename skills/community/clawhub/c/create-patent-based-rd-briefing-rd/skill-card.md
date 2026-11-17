## Description:

Create an evidence-bounded English patent-based R&D briefing from an authorized Excel workbook.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yuanzhian-patsnap](https://clawhub.ai/user/yuanzhian-patsnap)

### License/Terms of Use:

MIT

## Use Case:

External users, patent analysts, and R&D teams use this skill to screen authorized patent workbooks, organize reviewer-confirmed records by technology route and organization, and generate a self-contained HTML briefing for technical orientation and research planning.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Dependency installation and installer execution may affect the user's local environment.

Mitigation: Install in a dedicated environment, review requirements.txt before using dependency installation, and avoid elevated privileges.

Risk: Patent workbooks may contain confidential, licensed, or decision-sensitive information.

Mitigation: Process only workbooks the user is authorized to use and confirm confidentiality and distribution limits before generating or sharing outputs.

Risk: Workbook values, reviewer names, or custom topic configuration text could introduce unsafe spreadsheet or report content.

Mitigation: Treat workbook and configuration text as untrusted, review tagged workbooks before sharing, and keep generated reports within the documented review workflow.

Risk: Keyword matches or patent metadata can be mistaken for legal conclusions.

Mitigation: Use keyword hits only as discovery signals and require patent-professional review for material claim, status, FTO, validity, enforceability, and infringement questions.

## Reference(s):

- [PatSnap advanced patent search MCP server](https://open.patsnap.com/marketplace/mcp-servers/patent-search)
- [PatSnap patent briefing MCP server](https://open.patsnap.com/marketplace/mcp-servers/patent-briefing)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, Files, HTML, Markdown]

**Output Format:** [Markdown guidance with shell commands; local scripts produce tagged Excel workbooks and self-contained HTML briefings.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs are bounded to authorized local workbook evidence and require human review before briefing release.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata; artifact changelog top entry is 1.1.0-localized)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
