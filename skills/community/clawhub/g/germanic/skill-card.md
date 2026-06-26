## Description: <br>
Validate JSON data against schemas and compile to binary .grm files for schema-enforced data contracts used by AI agents. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[porco-rs](https://clawhub.ai/user/porco-rs) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill to validate structured JSON, generate or apply schemas, compile JSON into .grm files, and configure the GERMANIC CLI or MCP server for schema-enforced agent workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The GERMANIC CLI and MCP server are third-party local tools, and the MCP server exposes the local tool surface over stdio. <br>
Mitigation: Install only from a trusted germanic Homebrew tap or cargo package, verify the source or build when needed, and enable germanic serve-mcp only for trusted MCP clients. <br>
Risk: Compiled .grm files preserve valid string field content as data, so typed structure does not make string content trustworthy instructions. <br>
Mitigation: Treat validated fields as data in downstream agents and continue applying normal instruction-boundary and content-review controls. <br>


## Reference(s): <br>
- [GERMANIC ClawHub page](https://clawhub.ai/porco-rs/germanic) <br>
- [GERMANIC workflow examples](artifact/references/examples.md) <br>
- [GERMANIC schema types](artifact/references/schema-types.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration] <br>
**Output Format:** [Markdown with inline bash, JSON, and text examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The skill may guide an agent to run a local CLI that reads JSON inputs and writes .grm files.] <br>

## Skill Version(s): <br>
0.2.3 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
