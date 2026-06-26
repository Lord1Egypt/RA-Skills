## Description: <br>
Feishu Bitable Merger merges data from multiple Feishu Bitable tables into one target table. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[night556](https://clawhub.ai/user/night556) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and operations teams use this skill to consolidate Feishu Bitable records from multiple source tables into a target table, with optional field mapping and deduplication. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can read from and bulk-write records to Feishu Bitable tables, which may add many records to a target table without an automatic confirmation step. <br>
Mitigation: Install only from a trusted publisher, use a least-privilege Feishu app or account, double-check source and target URLs, and test on a non-production or backup table first. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/night556/feishu-bitable-merger) <br>
- [README](README.md) <br>
- [Skill definition](SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, API Calls, Text] <br>
**Output Format:** [Command-line status output and Feishu Bitable record writes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can bulk-add records to the target Feishu Bitable and optionally deduplicate records after merging.] <br>

## Skill Version(s): <br>
1.0.0 (source: release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
