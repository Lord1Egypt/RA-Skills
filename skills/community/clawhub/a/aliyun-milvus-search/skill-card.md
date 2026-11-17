## Description:

Helps agents use PyMilvus with AliCloud Milvus (serverless) to create collections, insert vectors, and run filtered similarity search.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cinience](https://clawhub.ai/user/cinience)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to configure PyMilvus access to AliCloud Milvus, create collections, insert sample vectors, and run filtered similarity search with bounded parameters.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Milvus credentials can be exposed if used with plaintext HTTP endpoints.

Mitigation: Use a TLS-protected Milvus endpoint and avoid the documented http:// form except for isolated local testing.

Risk: The quickstart performs mutating database operations by creating a collection and inserting records.

Mitigation: Run a minimal read-only connectivity check first, use a test collection or bounded scope, and confirm parameters before executing mutations.

Risk: Unpinned PyMilvus installation may pick up unexpected dependency changes.

Mitigation: Pin PyMilvus in the consuming environment and review dependency updates before installation.

Risk: Broad Milvus credentials could permit unintended data access or modification.

Mitigation: Use a narrowly scoped Milvus token with permissions limited to the target database and collection.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/cinience/skills/aliyun-milvus-search)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with Python and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include environment variable names, PyMilvus client code, collection/search parameters, and validation evidence paths.]

## Skill Version(s):

1.0.0 (source: SKILL.md frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
