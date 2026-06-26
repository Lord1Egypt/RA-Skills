## Description: <br>
原子化RAG知识库构建器 - 让AI真正学会一本书，而非只是看过。理工农医特化，方法论提炼，全网最好的开源专属知识库建立技能。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[simonstang](https://clawhub.ai/user/simonstang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, educators, researchers, and knowledge-management teams use this skill to convert PDFs and technical materials into atomic knowledge units for retrieval-augmented generation. It is aimed at personal knowledge bases, enterprise manuals, education content, research material, and STEM or medical documents that need structured retrieval. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The release includes an exposed GitHub-token-like repository URL and inconsistent repository URL metadata. <br>
Mitigation: Remove the credential-like URL, rotate any affected token, republish from a clean source, and verify repository links before installation. <br>
Risk: PDF content may be sent to OpenAI embeddings and retained in vector databases or JSON files. <br>
Mitigation: Avoid sensitive, regulated, proprietary, or medical documents unless the embedding backend, storage access, retention, and deletion process are controlled and documented. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/simonstang/atomic-rag-knowledge-base) <br>
- [README.md](README.md) <br>
- [PUBLISH.md](PUBLISH.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, JSON] <br>
**Output Format:** [Markdown guidance with Python examples, shell commands, and JSON knowledge atom structures.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces knowledge atoms, embeddings, vector database entries, saved JSON files, and RAG answer dictionaries depending on how the generated code is used.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter, package.json, server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
