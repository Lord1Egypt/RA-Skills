## Description: <br>
Attio API integration with managed OAuth for managing CRM objects, records, tasks, notes, comments, lists, meetings, call recordings, and workspace data. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[byungkyu](https://clawhub.ai/user/byungkyu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to work with Attio CRM data through Maton's OAuth-managed API proxy, including reading and modifying records, tasks, notes, comments, lists, meetings, and workspace data. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses a Maton API key and OAuth proxy to access Attio CRM data. <br>
Mitigation: Keep MATON_API_KEY private, install only when Maton is trusted for the intended workspace, and verify the selected Maton connection before use. <br>
Risk: Create, update, and delete operations can modify CRM records, tasks, notes, comments, lists, and related workspace data. <br>
Mitigation: Review the target resource and intended effect with the user before approving any write operation. <br>
Risk: Multiple Attio connections can route requests to the wrong workspace or account if the connection is ambiguous. <br>
Mitigation: Use the Maton-Connection header when multiple connections exist and confirm the connection before issuing requests. <br>
Risk: Some endpoints may fail or expose limited data when the OAuth connection lacks required scopes. <br>
Mitigation: Use the self/token and error responses to confirm available scopes, and request only the scopes needed for the user's task. <br>


## Reference(s): <br>
- [Attio skill page](https://clawhub.ai/byungkyu/attio-api) <br>
- [API gateway skill](https://clawhub.ai/byungkyu/api-gateway) <br>
- [Attio API Overview](https://docs.attio.com/rest-api/overview) <br>
- [Attio API Reference](https://docs.attio.com/rest-api/endpoint-reference) <br>
- [Records API](https://docs.attio.com/rest-api/endpoint-reference/records) <br>
- [Objects API](https://docs.attio.com/rest-api/endpoint-reference/objects) <br>
- [Tasks API](https://docs.attio.com/rest-api/endpoint-reference/tasks) <br>
- [Rate Limiting](https://docs.attio.com/rest-api/guides/rate-limiting) <br>
- [Pagination](https://docs.attio.com/rest-api/guides/pagination) <br>
- [Maton](https://maton.ai) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Code, Shell commands, Configuration instructions, API Calls] <br>
**Output Format:** [Markdown with inline JSON, Python, JavaScript, HTTP, and bash examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires network access, MATON_API_KEY, and an authorized Attio OAuth connection through Maton.] <br>

## Skill Version(s): <br>
1.0.5 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
