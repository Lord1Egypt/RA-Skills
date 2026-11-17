## Description:

原子化RAG知识库构建器 helps agents build retrieval-augmented generation knowledge bases from PDFs by splitting content into atomic knowledge units with STEM and medical processing support.

This skill is ready for commercial/non-commercial use.

## Publisher:

[simonstang](https://clawhub.ai/user/simonstang)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, educators, researchers, and knowledge-management teams use this skill to turn PDF books, papers, manuals, and training materials into searchable atomic RAG knowledge bases. It is especially oriented toward STEM and medical content where formulas, derivations, tables, and structured methods need to remain connected to their source context.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release evidence reports an exposed GitHub token in the artifact.

Mitigation: Revoke and remove the token before installation or redistribution, and review release contents for any other embedded credentials.

Risk: PDF contents may be sent to configured embedding providers and stored in vector databases.

Mitigation: Only process documents approved for the selected provider and database, and define retention, deletion, and access controls for stored knowledge bases.

Risk: Dependencies and integrations for PDF parsing, OCR, embeddings, and vector databases increase the operational review surface.

Mitigation: Install in an isolated environment, pin and audit dependencies, and review provider configuration before processing sensitive documents.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/simonstang/skills/atomic-rag-knowledge-base)
- [README.md](artifact/README.md)
- [SKILL.md](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown guidance with Python examples, shell commands, and structured knowledge-atom schemas]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces guidance and code-oriented workflows for PDF extraction, atomic chunking, embedding generation, vector storage, and RAG retrieval.]

## Skill Version(s):

1.0.0 (source: server release evidence, SKILL.md frontmatter, package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
