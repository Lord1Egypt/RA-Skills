## Description: <br>
Scans websites for AI agent readiness across discoverability, content accessibility, bot access control, protocol discovery, and commerce checks, then produces scored reports with fix suggestions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[maooson](https://clawhub.ai/user/maooson) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, site operators, and agent-readiness reviewers use this skill to check whether a website exposes signals such as robots.txt, llms.txt, MCP discovery, agent skills, API catalogs, OAuth discovery, and commerce protocol support. The skill helps produce a readiness score and practical remediation guidance for a user-named target site. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The scanner makes HTTP requests to websites named by the user. <br>
Mitigation: Scan only public or explicitly authorized targets, and avoid internal or sensitive systems unless authorization is clear. <br>
Risk: Generated HTML reports can include unsafe unescaped content from scanned sites. <br>
Mitigation: Use JSON or text output for untrusted targets, and treat generated HTML reports as unsafe until output escaping is fixed. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/maooson/agent-ready-scanner) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/maooson) <br>
- [isitagentready.com](https://isitagentready.com) <br>
- [llms.txt](https://llmstxt.org/) <br>
- [Model Context Protocol](https://modelcontextprotocol.io/) <br>
- [Agent Skills](https://agentskills.io/) <br>


## Skill Output: <br>
**Output Type(s):** [text, json, html, configuration, guidance] <br>
**Output Format:** [Text summaries, JSON scan reports, and local HTML report files with scored findings and remediation snippets.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports are generated from HTTP checks against a user-specified website and may include copied response details and suggested configuration snippets.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
