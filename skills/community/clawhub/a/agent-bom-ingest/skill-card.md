## Description: <br>
Validate and ingest operator-pushed agent-bom inventory JSON from AWS, Azure, GCP, Snowflake, CMDB, or endpoint collectors so users can produce local findings, graphs, policy checks, provenance review, or auditor-ready exports without giving agent-bom direct cloud credentials. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[msaad00](https://clawhub.ai/user/msaad00) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, security engineers, and operators use this skill when they already have canonical agent-bom inventory JSON and need local validation, scanning, graphing, policy review, provenance checks, or JSON/SARIF/HTML/Markdown exports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Inventory files may contain sensitive environment names, topology, or security posture data. <br>
Mitigation: Review inventory files before scanning and rely on schema validation plus redaction before display or export. <br>
Risk: Optional AGENT_BOM_API_KEY and AGENT_BOM_PUSH_URL settings can push results outside the local environment. <br>
Mitigation: Enable them only for an operator-owned control plane, and never paste or print API tokens. <br>
Risk: Optional vulnerability and advisory enrichment can contact OSV or GitHub Advisory endpoints. <br>
Mitigation: Use the local-only workflow when outbound network access is not approved. <br>


## Reference(s): <br>
- [agent-bom homepage](https://github.com/msaad00/agent-bom) <br>
- [agent-bom PyPI package](https://pypi.org/project/agent-bom/) <br>
- [OSV vulnerability API](https://api.osv.dev/v1) <br>
- [GitHub Advisory enrichment API](https://api.github.com/advisories) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, markdown] <br>
**Output Format:** [Markdown guidance with inline bash commands and export-format choices] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The skill guides local validation and scan/export workflows that can produce JSON, SARIF, HTML, Markdown, CycloneDX, or SPDX outputs through agent-bom.] <br>

## Skill Version(s): <br>
0.89.2 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
