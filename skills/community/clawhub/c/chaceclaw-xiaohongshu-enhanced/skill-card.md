## Description: <br>
小红书（RED/XHS）自动化助手，帮助 agents use xiaohongshu-mcp for login, publishing, search, note browsing, engagement, profile analysis, and content planning workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ling-qian](https://clawhub.ai/user/ling-qian) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External creators, operators, and developers use this skill to operate Xiaohongshu workflows through a configured MCP service, including content publishing, search, engagement, account checks, and content strategy support. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles Xiaohongshu session cookies and tokens for an active account. <br>
Mitigation: Install only with a trusted xiaohongshu-mcp package, keep the MCP endpoint local, protect cookie and token files like passwords, and prefer a test account. <br>
Risk: The skill can publish posts and perform account actions such as comments, likes, collections, account switching, batch operations, and data export. <br>
Mitigation: Require explicit user confirmation before each public or account-changing action, and preview publish/comment content before execution. <br>
Risk: Automation, scraping, and broad triggers can trigger platform rate limits, account restrictions, or unintended collection. <br>
Mitigation: Follow the bundled rate-limit guide, avoid batch actions unless necessary, verify login and account state before operations, and stop after rate-limit or security errors. <br>
Risk: Generated public content may violate platform, legal, brand, medical, financial, or privacy rules. <br>
Mitigation: Use the bundled compliance checklist before publishing and review sensitive claims, external links, contact details, personal data, and media rights. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ling-qian/chaceclaw-xiaohongshu-enhanced) <br>
- [Publisher profile](https://clawhub.ai/user/ling-qian) <br>
- [Xiaohongshu MCP rate-limit guide](xhs-rate-limits.md) <br>
- [Xiaohongshu content compliance checklist](xhs-compliance.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline code, shell commands, configuration snippets, checklists, and MCP tool-call instructions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may include public-post drafts, comments, search and analysis plans, account setup steps, and operational checklists.] <br>

## Skill Version(s): <br>
1.0.1 (source: server-resolved release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
