## Description: <br>
AKY-ES helps agents use Elasticsearch 8.17 to store, index, search, retrieve, and manage persistent data. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wangfromchu-ai](https://clawhub.ai/user/wangfromchu-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agents and developers use this skill to operate Elasticsearch-backed memory and document indexes, including CRUD, search, bulk import, and service status workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Automatic fallback to Elastic Cloud can store notes, documents, or memory data outside the local machine. <br>
Mitigation: Verify ES_URL and credential variables before storing data, and avoid or disable cloud fallback when strictly local storage is required. <br>
Risk: Write, bulk import, and delete commands can change or remove indexed data. <br>
Mitigation: Review target index names and JSON payloads before running commands, especially when using sensitive or production data. <br>


## Reference(s): <br>
- [AKY-ES on ClawHub](https://clawhub.ai/wangfromchu-ai/skills/aky-es) <br>
- [Elasticsearch documentation](https://www.elastic.co/guide/en/elasticsearch/reference/current/index.html) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Code, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands, Python examples, and Elasticsearch JSON payloads] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include commands that read, write, import, search, or delete Elasticsearch indexes.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
