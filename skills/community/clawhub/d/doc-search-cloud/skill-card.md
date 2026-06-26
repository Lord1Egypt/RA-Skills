## Description: <br>
doc-search helps agents vectorize Word, Markdown, PDF, and text documents, persist local indexes, and retrieve relevant passages with vector or hybrid search. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cloudcba](https://clawhub.ai/user/cloudcba) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to index local document collections and retrieve relevant passages for document search, semantic lookup, and vector-store management workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Indexed document text and query cache data can remain in the local chroma_data store. <br>
Mitigation: Use the skill only in trusted project directories, avoid indexing sensitive documents unless local retention is acceptable, and clear or delete the local store when finished. <br>
Risk: The vectorizer loads local pickle persistence files, which can execute unsafe data if those files are modified by an untrusted party. <br>
Mitigation: Do not use the skill where untrusted users or processes can modify persistence files; prefer a safer storage format before broader deployment. <br>
Risk: The clear_collection behavior deletes local persistence files. <br>
Mitigation: Confirm the target collection and storage directory before clearing a collection. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/cloudcba/doc-search-cloud) <br>
- [Publisher profile](https://clawhub.ai/user/cloudcba) <br>


## Skill Output: <br>
**Output Type(s):** [text, code, configuration, guidance] <br>
**Output Format:** [Markdown guidance with Python code examples and JSON-like result objects] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Search results include retrieved content, similarity scores, and metadata when the vectorizer is called.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata; artifact frontmatter says v3.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
