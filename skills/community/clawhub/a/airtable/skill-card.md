## Description: <br>
Airtable API integration with managed OAuth for reading, creating, updating, deleting, and querying Airtable records. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[byungkyu](https://clawhub.ai/user/byungkyu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to work with Airtable bases, tables, and records through Maton-managed OAuth. It supports record lookup, filtered queries, connection selection, and approved create, update, or delete operations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses Maton to broker access to Airtable data through a sensitive MATON_API_KEY. <br>
Mitigation: Install only when Maton is trusted for this access, keep the API key private, and scope Airtable connections to the intended account. <br>
Risk: Create, update, and delete operations can change Airtable records in the connected account. <br>
Mitigation: Review the target base, table, records, and intended effect before approving any write operation. <br>
Risk: Multiple Airtable connections can cause requests to affect the wrong account. <br>
Mitigation: Use the Maton-Connection header when more than one Airtable connection exists. <br>


## Reference(s): <br>
- [Airtable Skill on ClawHub](https://clawhub.ai/byungkyu/airtable) <br>
- [Publisher Profile](https://clawhub.ai/user/byungkyu) <br>
- [Maton](https://maton.ai) <br>
- [Airtable API Overview](https://airtable.com/developers/web/api/introduction) <br>
- [Airtable List Records](https://airtable.com/developers/web/api/list-records) <br>
- [Airtable Create Records](https://airtable.com/developers/web/api/create-records) <br>
- [Airtable Update Record](https://airtable.com/developers/web/api/update-record) <br>
- [Airtable Delete Record](https://airtable.com/developers/web/api/delete-record) <br>
- [Airtable Formula Reference](https://support.airtable.com/docs/formula-field-reference) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, code, shell commands, configuration] <br>
**Output Format:** [Markdown with inline API paths and Python or JavaScript examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires network access, MATON_API_KEY, and a connected Airtable OAuth account.] <br>

## Skill Version(s): <br>
1.0.7 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
