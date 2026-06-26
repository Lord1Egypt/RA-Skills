## Description: <br>
Syncs data between Feishu Bitable tables and external sources, including one-way sync, two-way conflict handling, CSV imports, and scheduled sync markers. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ramlee77](https://clawhub.ai/user/ramlee77) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agents supporting Feishu Bitable users use this skill to read, transform, create, update, and delete records while syncing data between tables or importing external data such as CSV rows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Bulk sync operations can create, update, overwrite, or delete Feishu Bitable records at scale. <br>
Mitigation: Use least-privilege credentials scoped to specific bases and tables, then require a dry-run summary and explicit confirmation before any write or delete action. <br>
Risk: Incorrect field mapping or conflict resolution can corrupt destination records. <br>
Mitigation: Validate field types and unique identifiers, preview record-level changes, and back up or export affected tables before syncing. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ramlee77/feishu-bitable-sync) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, configuration, API calls, JSON] <br>
**Output Format:** [Markdown with JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Feishu app tokens, table IDs, matching field types, and user review before write or delete actions.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
