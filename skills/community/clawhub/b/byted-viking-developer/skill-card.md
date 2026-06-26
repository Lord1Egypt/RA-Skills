## Description: <br>
Guides developers who integrate and use Viking SDKs across VikingDB, KnowledgeBase, and Memory, including installation, authentication, API calls, and troubleshooting. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[volcengine-skills](https://clawhub.ai/user/volcengine-skills) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to find implementation guidance for VikingDB vector search, KnowledgeBase RAG workflows, and Viking Memory SDK integrations in Python, Go, and Java. It supports business code development, API usage questions, and issue diagnosis for Viking services. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Examples may encourage unsafe handling of AK/SK values, API keys, temporary links, or sensitive memory/session responses. <br>
Mitigation: Use HTTPS/TLS, store secrets in a secrets manager, avoid logging full responses or temporary links, and review copied examples before production use. <br>
Risk: SDK examples include mutating update and delete operations that can affect Viking resources if filters or identifiers are wrong. <br>
Mitigation: Verify collection, index, document, session, and filter parameters before running update or delete tasks. <br>
Risk: Guidance may involve sending documents, images, prompts, user profiles, or memory data to Viking services. <br>
Mitigation: Send sensitive data only when privacy, retention, and access-control requirements allow it. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/volcengine-skills/byted-viking-developer) <br>
- [VikingDB Python SDK guide](artifact/resources/vikingdb-python-sdk.md) <br>
- [VikingDB Go SDK guide](artifact/resources/vikingdb-go-sdk.md) <br>
- [VikingDB Java SDK guide](artifact/resources/vikingdb-java-sdk.md) <br>
- [KnowledgeBase Python SDK guide](artifact/resources/knowledge-python-sdk.md) <br>
- [Memory Python SDK guide](artifact/resources/memory-python-sdk.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with SDK examples, commands, configuration notes, and troubleshooting guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Documentation-only guidance for agent responses; examples may require user-provided Viking service credentials and project settings.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
