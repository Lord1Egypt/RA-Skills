## Description: <br>
Track 3D printing filament inventory locally, including spool additions, usage logging, stock checks, searches, and spending reports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[newageinvestments25-byte](https://clawhub.ai/user/newageinvestments25-byte) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, makers, and 3D printing operators use this skill to maintain a local filament inventory, record spool usage, find low stock, search materials, and produce spending or stock reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Filament costs, storage locations, and free-text notes are stored locally in plain JSON. <br>
Mitigation: Do not record sensitive personal information in notes or location fields on shared machines; review local file access as needed. <br>
Risk: Inventory update commands modify local spool records and can mark spools finished or reduce remaining weight. <br>
Mitigation: Review command arguments before running update scripts and keep a backup if the inventory is operationally important. <br>


## Reference(s): <br>
- [Filament Materials Guide](references/materials.md) <br>
- [Filament Vault ClawHub Page](https://clawhub.ai/newageinvestments25-byte/filament-vault) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Text, JSON] <br>
**Output Format:** [Markdown guidance with inline shell commands; scripts emit plain text tables, reports, or JSON when requested.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Stores inventory data locally at ~/.openclaw/workspace/filament-vault/inventory.json.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
