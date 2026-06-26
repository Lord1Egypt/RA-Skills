## Description: <br>
CorpusGraph helps agents ingest documents, extract entities, search structured content, and map relationships across document corpora through the Ingestigate platform. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aingestigate](https://clawhub.ai/user/aingestigate) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and analysts use CorpusGraph to turn varied document collections into searchable text, structured records, extracted entities, and relationship evidence that an agent can query without parsing raw files directly. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends selected documents and corpus queries to the Ingestigate platform for ETL, indexing, entity extraction, search, and graph analysis. <br>
Mitigation: Use it only with corpora approved for the provider and deployment environment, and avoid sensitive or regulated data unless organizational terms and controls allow it. <br>
Risk: Corpus results may be incomplete while processing is still running. <br>
Mitigation: Check readiness and processing status before drawing conclusions, and tell the user when returned results may be incomplete. <br>
Risk: The skill depends on short-lived Ingestigate credentials and authenticated API access. <br>
Mitigation: Configure tokens only in secure skill settings, do not ask users to paste secrets into chat, and refresh expired tokens through the provider workflow. <br>


## Reference(s): <br>
- [CorpusGraph](https://ingestigate.com/corpusgraph) <br>
- [Ingestigate Platform](https://ingestigate.com) <br>
- [Authenticated API Guide](https://app1.ingestigate.com/api/agent/guide) <br>
- [ClawHub Skill Page](https://clawhub.ai/aingestigate/corpusgraph) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with API request examples and concise analysis] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires configured Ingestigate credentials; API responses should be treated as the source of truth for corpus status, search results, entity extraction, and relationship evidence.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
