## Description: <br>
Analyzes ByteHouse databases through a ByteHouse MCP server to produce schema, data asset catalog, and lineage reports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[volcengine-skills](https://clawhub.ai/user/volcengine-skills) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and data engineers use this skill to inspect ByteHouse table schemas, generate data asset inventories, and identify simple table and column lineage patterns. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill runs unpinned remote code with the full environment. <br>
Mitigation: Install only if you trust the Volcengine MCP repository and keep the runtime environment limited to the required BYTEHOUSE_* variables. <br>
Risk: Generated reports can contain sensitive ByteHouse schema and metadata. <br>
Mitigation: Use a read-only ByteHouse account, avoid shared or synced output directories, and delete generated JSON reports when they are no longer needed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/volcengine-skills/byted-bytehouse-data-asset-analyzer) <br>


## Skill Output: <br>
**Output Type(s):** [JSON files, Shell commands, Configuration guidance] <br>
**Output Format:** [Markdown guidance with shell commands and generated JSON reports] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes schema, catalog, and lineage JSON files to a local output directory.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and release changelog) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
