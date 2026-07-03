## Description: <br>
Digital Finance Presentation Skill generates enterprise digital-finance presentations as PPTX files and macOS Keynote documents, with templates for SAP-style financial digitalization, valuation, ESG, and RPA reports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yjkj999999](https://clawhub.ai/user/yjkj999999) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers, consultants, and enterprise finance teams use this skill to create professional decks for enterprise summits, financial digitalization narratives, valuation reports, ESG carbon asset reporting, and RPA case presentations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can give an agent broad persistent control over local Keynote documents. <br>
Mitigation: Use it on macOS systems where agent control of Keynote is approved, work on copies of decks, and review document changes before saving or exporting. <br>
Risk: The installer can add a Claude Desktop MCP server configuration and install Python dependencies. <br>
Mitigation: Inspect the MCP configuration change and dependency installation commands before running the installer. <br>
Risk: Presentation content may include confidential business or financial information. <br>
Mitigation: Use only assistant environments approved for the data being placed into generated or edited presentations. <br>


## Reference(s): <br>
- [Model Context Protocol](https://modelcontextprotocol.io/) <br>
- [Keynote AppleScript Guide](https://developer.apple.com/library/archive/documentation/AppleApplications/Conceptual/Keynote_Scripting_Guide/) <br>
- [python-pptx Documentation](https://python-pptx.readthedocs.io/) <br>
- [Design Guide](artifact/templates/design_guide.md) <br>
- [Launch Event Outline](artifact/templates/launch_event_outline.md) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Code, Shell commands, Configuration instructions, Files] <br>
**Output Format:** [Markdown guidance with inline shell commands, Python code workflows, JSON configuration, PPTX files, and Keynote documents] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated decks may depend on python-pptx for PPTX output or macOS Keynote automation for native .key output.] <br>

## Skill Version(s): <br>
6.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
