## Description: <br>
The official search utility for Agnxi.com, a directory of AI agent tools, MCP servers, and skills. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[doanbactam](https://clawhub.ai/user/doanbactam) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Agents, developers, and operators use this skill to search Agnxi for relevant agent skills, MCP servers, and tool resources, then review the returned links before using or installing them. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill contacts Agnxi.com when used and depends on live sitemap availability and content. <br>
Mitigation: Use it in environments where outbound access to Agnxi.com is acceptable, and treat returned links as candidates to review before installation or use. <br>
Risk: The release has unavailable server-resolved provenance and the README contains a placeholder repository URL. <br>
Mitigation: Verify the publisher profile and source before relying on the skill in sensitive workflows. <br>
Risk: Unsafe query handling by a calling agent could expose shell-injection risk if raw user text is interpolated into commands. <br>
Mitigation: Pass queries as process arguments rather than raw shell text, as recommended by the security guidance. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/doanbactam/agnxi-search-skill) <br>
- [Agnxi directory](https://agnxi.com) <br>
- [Agnxi sitemap](https://agnxi.com/sitemap.xml) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [Plain text search status and matching URLs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Fetches the live Agnxi sitemap and prints up to 10 matching links for a query.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata; artifact frontmatter reports 1.1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
