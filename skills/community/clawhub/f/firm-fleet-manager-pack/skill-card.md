## Description: <br>
Multi-instance Gateway fleet management pack for status monitoring, dynamic add/remove operations, broadcast commands, configuration sync, and fleet inventory. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[romainsantoli-web](https://clawhub.ai/user/romainsantoli-web) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and operators use this skill to monitor and manage multiple Gateway instances, including fleet health checks, inventory, scaling, command broadcast, and configuration synchronization. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Fleet-management actions can trigger broad operational changes without documented scoping, confirmations, or rollback safeguards. <br>
Mitigation: Use only in authorized environments, confirm the exact actions executed by mcp-openclaw-extensions, require operator confirmation and dry runs where possible, keep audit logs, and prepare rollback plans before remove, broadcast, or sync operations. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/romainsantoli-web/firm-fleet-manager-pack) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration] <br>
**Output Format:** [Markdown with tool names and YAML usage examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires mcp-openclaw-extensions >= 3.0.0.] <br>

## Skill Version(s): <br>
1.0.0 (source: release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
