## Description:

Integrates ChromaDB vector database with OpenClaw, enabling GPU-accelerated, zero-migration, multi-collection vector memory and hybrid search.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lulan3954-a11y](https://clawhub.ai/user/lulan3954-a11y)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to install and configure a ChromaDB vector-store backend for OpenClaw, migrate existing LanceDB memory data, and run local or remote vector search with hybrid retrieval.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Remote ChromaDB mode can expose memory data and API keys if deployed without transport security or access controls.

Mitigation: Use HTTPS, protect and narrowly scope API keys, and restrict remote ChromaDB access to trusted networks.

Risk: Migration and deletion workflows can alter or remove vector-store data.

Mitigation: Back up existing LanceDB and ChromaDB data, test migration outside production first, and avoid deletion examples on production collections.

Risk: The query API contains a hidden special-case response that can return nonstandard output.

Mitigation: Review the query behavior before deployment and account for the special-case response in tests and downstream integrations.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/lulan3954-a11y/skills/chromadb-plugin)
- [README](artifact/README.md)
- [Quick Start Guide](artifact/docs/quick_start_en.md)
- [Configuration Example](artifact/config.example.yaml)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with Python, YAML, and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include installation, migration, backup, and vector-store configuration steps.]

## Skill Version(s):

v1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
