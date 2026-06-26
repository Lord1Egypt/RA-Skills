## Description: <br>
MCP 2025-11-25 specification compliance audit pack that validates elicitation, tasks, resources and prompts, audio content, JSON Schema 2020-12, SSE transport, and icon metadata compliance across seven specialized audit tools. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[romainsantoli-web](https://clawhub.ai/user/romainsantoli-web) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and engineers use this skill to audit MCP server or agent configurations against the MCP 2025-11-25 specification, including protocol features such as elicitation, durable tasks, SSE resumption, JSON Schema dialects, audio content, and icon metadata. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The audit guidance depends on the expected MCP protocol version and OpenClaw extension dependency. <br>
Mitigation: Before running audits, verify mcp-openclaw-extensions >= 3.0.0 and confirm the target configuration is intended for MCP Protocol Version 2025-11-25. <br>
Risk: Compliance audit output can be incomplete or misleading if broad or unintended configuration files are supplied. <br>
Mitigation: Provide only the specific MCP configuration files you want checked and review the results before relying on them for compliance decisions. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/romainsantoli-web/firm-spec-compliance-pack) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration] <br>
**Output Format:** [Markdown with YAML and command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces audit-oriented guidance for MCP configuration checks; no executable code is bundled in the artifact.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
