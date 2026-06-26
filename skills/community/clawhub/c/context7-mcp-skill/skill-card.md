## Description: <br>
Query up-to-date library documentation and code examples using Context7 MCP. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jolestar](https://clawhub.ai/user/jolestar) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill to resolve library identifiers and query current, version-specific documentation and code examples for npm packages, Python libraries, and other programming ecosystems. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends documentation queries to the external Context7 MCP endpoint. <br>
Mitigation: Use it for public library documentation questions and avoid sending secrets, proprietary code, or sensitive internal details. <br>
Risk: The skill may create a local fixed command alias for Context7 MCP access. <br>
Mitigation: Install only when the user trusts the uxc tooling and the Context7 MCP endpoint, and stop for maintainer review if the fixed command name conflicts. <br>


## Reference(s): <br>
- [Context7 MCP endpoint](https://mcp.context7.com/mcp) <br>
- [Usage patterns](references/usage-patterns.md) <br>
- [ClawHub skill page](https://clawhub.ai/jolestar/context7-mcp-skill) <br>
- [uxc skill prerequisite](https://github.com/holon-run/uxc/tree/main/skills/uxc) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and MCP query results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include command setup steps, resolved library IDs, documentation excerpts, and code examples returned by Context7.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
