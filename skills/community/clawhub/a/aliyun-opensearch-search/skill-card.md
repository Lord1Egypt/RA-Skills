## Description: <br>
Use when working with OpenSearch vector search edition via the Python SDK (ha3engine) to push documents and run HA/SQL searches. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cinience](https://clawhub.ai/user/cinience) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to configure Alibaba Cloud OpenSearch vector search access, push bounded document updates, and run HA or SQL searches for RAG and retrieval workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The bundled quickstart can write sample documents to a live OpenSearch data source. <br>
Mitigation: Use a test data source first, confirm the operation is intended to be mutating, and avoid running the quickstart against production unless sample document writes are desired. <br>
Risk: OpenSearch credentials are provided through environment variables and the quickstart evidence notes under-guarded credential handling. <br>
Mitigation: Use least-privilege credentials, avoid logging secrets, and verify HTTPS/TLS before providing credentials. <br>


## Reference(s): <br>
- [Skill source list](references/sources.md) <br>
- [ClawHub skill page](https://clawhub.ai/cinience/aliyun-opensearch-search) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown with Python and bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include environment variable setup, quickstart commands, validation steps, and OpenSearch API usage patterns.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
