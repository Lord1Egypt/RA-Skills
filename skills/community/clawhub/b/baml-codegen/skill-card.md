## Description:

Generates complete BAML files for type-safe LLM extraction, classification, RAG, and agent workflows, including schemas, functions, clients, tests, and framework integration code.

This skill is ready for commercial/non-commercial use.

## Publisher:

[killerapp](https://clawhub.ai/user/killerapp)

### License/Terms of Use:

Apache-2.0

## Use Case:

Developers and engineers use this skill to generate BAML schemas, functions, clients, tests, and integration code from natural-language requirements for extraction, classification, RAG, and agent workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The mandatory BAML generation workflow can execute project-defined shell hooks through generator configuration.

Mitigation: Inspect baml_src/generators.baml before each generation run, avoid or explicitly approve on_generate hooks, and run generation in a low-privilege sandbox.

Risk: Examples and workflows may involve invoices, receipts, resumes, images, chat history, or other sensitive data sent to external model providers.

Mitigation: Use consent, redaction, retention controls, and approved providers before sending sensitive data to external services.

Risk: Generated code behavior depends on the installed BAML package and CLI versions.

Mitigation: Pin BAML package and CLI versions before generating clients or integration code.

## Reference(s):

- [BAML Reference Guide](references/BAML-REFERENCE-SOURCE.md)
- [Provider Configuration Reference](references/providers.md)
- [BAML Types and Schemas Reference](references/types-and-schemas.md)
- [Validation Patterns Reference](references/validation.md)
- [BAML Pattern Library](references/patterns.md)
- [BAML Philosophy](references/philosophy.md)
- [MCP Interface and Query Strategy](references/mcp-interface.md)
- [Python and BAML Reference](references/languages-python.md)
- [TypeScript and BAML Reference](references/languages-typescript.md)
- [LangGraph and BAML Integration Reference](references/frameworks-langgraph.md)
- [BoundaryML BAML Releases](https://github.com/BoundaryML/baml/releases)
- [BAML VS Code Extension](https://marketplace.visualstudio.com/items?itemName=boundary.baml-extension)

## Skill Output:

**Output Type(s):** [Code, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with BAML, test, integration code, shell command, and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated artifacts may target Python, TypeScript, Ruby, Go, and common web or agent frameworks.]

## Skill Version(s):

2.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
