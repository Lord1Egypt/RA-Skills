## Description: <br>
Use when working with AliCloud Milvus (serverless) with PyMilvus to create collections, insert vectors, and run filtered similarity search. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cinience](https://clawhub.ai/user/cinience) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to configure and validate AliCloud Milvus vector search workflows with PyMilvus, including collection creation, vector insertion, and filtered similarity search for Claude Code/Codex retrieval flows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Milvus credentials may grant broader database access than the task requires. <br>
Mitigation: Use a least-privilege Milvus token and keep MILVUS_TOKEN out of logs, prompts, and committed files. <br>
Risk: The quickstart can create collections and insert records in the configured database. <br>
Mitigation: Run the quickstart against a test database or collection unless the user intentionally wants those changes. <br>


## Reference(s): <br>
- [Source list](references/sources.md) <br>
- [ClawHub skill page](https://clawhub.ai/cinience/aliyun-milvus-search) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, shell commands, configuration] <br>
**Output Format:** [Markdown with Python and bash snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [None] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
