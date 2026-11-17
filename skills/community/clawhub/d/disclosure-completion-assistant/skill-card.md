## Description:

A bilingual patent disclosure completion assistant for patent agencies, inventors, and R&D teams that packages a standalone customer-facing HTML guide for collecting invention information, applying AI-assisted completion, and generating a structured invention disclosure draft for patent attorney review.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yuanzhian-patsnap](https://clawhub.ai/user/yuanzhian-patsnap)

### License/Terms of Use:

MIT-0

## Use Case:

Patent agencies, inventors, and R&D teams use this skill to turn incomplete invention notes, product descriptions, research summaries, or chat records into a more structured bilingual patent disclosure draft for attorney review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles confidential or pre-filing invention information without enough documented data-handling safeguards.

Mitigation: Review organizational confidentiality, retention, and approved data-flow controls before using it with sensitive invention data.

Risk: The security evidence reports a browser XSS risk in the generated draft view.

Mitigation: Treat the HTML as a local demo and avoid untrusted HTML-like input until draft rendering is fixed to sanitize output or use textContent.

Risk: Full functionality depends on PatSnap MCP setup, account authorization, and enabled MCP tools.

Mitigation: Complete the documented MCP setup and connectivity check before relying on live patent, literature, or database-backed results.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/yuanzhian-patsnap/skills/disclosure-completion-assistant)
- [Primary HTML Disclosure Guide](artifact/assets/disclosure-guide.html)
- [PatSnap Open Platform](https://open.zhihuiya.com/)
- [PatSnap Authentication Guide](https://open.zhihuiya.com/devportal/guides/authentication)
- [PatSnap MCP Server Marketplace](https://open.zhihuiya.com/marketplace/mcp-servers)

## Skill Output:

**Output Type(s):** [Guidance, Text, Files, Configuration instructions]

**Output Format:** [Markdown guidance and standalone HTML disclosure guide with generated disclosure draft text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Bilingual zh-CN/en workflow; full live-data functionality depends on PatSnap MCP account authorization and enabled MCP tools.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
