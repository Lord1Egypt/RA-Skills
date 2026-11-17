## Description:

SAP Enterprise Ultra-Wide Presentation Generator with AI-Empowered methodology for professional presentations for enterprise summits, financial digitalization, valuation reports, SAP Business AI narratives, RPA cases, ESG carbon asset management, and digital finance analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yjkj999999](https://clawhub.ai/user/yjkj999999)

### License/Terms of Use:

MIT

## Use Case:

Developers and business presentation authors use this skill to generate SAP-style digital finance presentations, valuation reports, ESG carbon asset management decks, and RPA case-study slides as PPTX files or macOS Keynote documents.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can grant a local MCP server control over Keynote and allow it to create, read, modify, save, export, and delete presentation content.

Mitigation: Install only in environments where this local automation access is acceptable, and review generated or modified presentations before relying on them.

Risk: The installer can change local files or configuration, including Claude Desktop MCP configuration.

Mitigation: Review the installer before running it and avoid running it in an environment with sensitive MCP configuration.

Risk: The security scan reports unsafe AppleScript handling that could run commands.

Mitigation: Treat the AppleScript injection issue as needing a fix before normal use.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/yjkj999999/skills/dfp-skill)
- [Model Context Protocol Documentation](https://modelcontextprotocol.io/)
- [Apple Keynote AppleScript Guide](https://developer.apple.com/library/archive/documentation/AppleApplications/Conceptual/Keynote_Scripting_Guide/)
- [python-pptx Documentation](https://python-pptx.readthedocs.io/)

## Skill Output:

**Output Type(s):** [Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline shell commands and generated presentation files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can produce PPTX files cross-platform and Keynote files on macOS with local automation permissions.]

## Skill Version(s):

6.0.0 (source: frontmatter, release evidence, clawhub.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
