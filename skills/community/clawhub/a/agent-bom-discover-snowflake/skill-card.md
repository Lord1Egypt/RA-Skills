## Description: <br>
Discover Snowflake Cortex, Snowpark, notebook, Streamlit, MCP, and AI-observability assets from the operator's environment, emit canonical agent-bom inventory JSON, and scan it without giving agent-bom long-lived Snowflake credentials. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[msaad00](https://clawhub.ai/user/msaad00) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to inventory Snowflake AI and Cortex infrastructure from their own environment, produce schema-valid agent-bom inventory JSON, and optionally scan that inventory for findings without granting agent-bom long-lived Snowflake credentials. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Snowflake credentials could be exposed if pasted into chat or displayed during setup. <br>
Mitigation: Use the operator's existing Snowflake SSO, OAuth, or key-pair authentication context and do not request passwords, private key contents, passphrases, or OAuth tokens in chat. <br>
Risk: Discovery could access more Snowflake resources than intended if broad accounts, warehouses, databases, or roles are used. <br>
Mitigation: Run only against operator-approved Snowflake accounts and use read-only roles scoped to the intended inventory. <br>
Risk: Inventory output may contain sensitive environment metadata. <br>
Mitigation: Write inventory only to an operator-selected local path, preserve credential redaction, and stop if schema validation fails. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/msaad00/agent-bom-discover-snowflake) <br>
- [agent-bom source](https://github.com/msaad00/agent-bom) <br>
- [agent-bom on PyPI](https://pypi.org/project/agent-bom/) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, JSON] <br>
**Output Format:** [Markdown guidance with bash command examples and JSON inventory outputs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Discovery-only by default; writes operator-selected inventory JSON and optional findings JSON.] <br>

## Skill Version(s): <br>
0.89.2 (source: SKILL.md frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
