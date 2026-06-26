## Description: <br>
Use OpenSearch vector search edition via the Python SDK (ha3engine) to push documents and run HA/SQL searches for RAG and vector retrieval pipelines in Claude Code/Codex. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cinience](https://clawhub.ai/user/cinience) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to configure Alibaba Cloud OpenSearch vector search workflows, push documents, and run HA/SQL searches for RAG or vector retrieval pipelines. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses cloud credentials and the quickstart configures the OpenSearch SDK with HTTP. <br>
Mitigation: Use least-privilege credentials and require HTTPS/TLS before running examples. <br>
Risk: The quickstart pushes sample documents to the configured remote OpenSearch index. <br>
Mitigation: Run first against a non-production datasource with explicit parameters and confirm the mutation scope before using production data. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/cinience/alicloud-ai-search-opensearch) <br>
- [Artifact source list](artifact/references/sources.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with Python and bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include API response summaries and saved evidence under output/alicloud-ai-search-opensearch/ when run by an agent.] <br>

## Skill Version(s): <br>
1.0.3 (source: ClawHub release metadata; artifact frontmatter reports 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
