## Description: <br>
Memory infrastructure audit pack for pgvector configuration validation and knowledge graph integrity checks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[romainsantoli-web](https://clawhub.ai/user/romainsantoli-web) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and operators use this skill to audit memory infrastructure, including pgvector extension settings and knowledge graph integrity. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated audit guidance or findings may be incorrect or incomplete. <br>
Mitigation: Review audit results against the actual pgvector and knowledge graph configuration before changing memory infrastructure. <br>
Risk: The skill invokes audit tools against caller-provided configuration paths. <br>
Mitigation: Confirm each config_path targets the intended file and review commands before execution in operator environments. <br>
Risk: The skill depends on mcp-openclaw-extensions >= 3.0.0. <br>
Mitigation: Verify the installed extension version and source before enabling the skill. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/romainsantoli-web/firm-memory-audit-pack) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with YAML and inline command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires mcp-openclaw-extensions >= 3.0.0 and a configuration path for each audit tool.] <br>

## Skill Version(s): <br>
1.0.0 (source: SKILL.md frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
