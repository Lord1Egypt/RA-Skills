## Description: <br>
Generates BAML code for type-safe LLM extraction, classification, RAG, and agent workflows, including .baml source, typed clients, tests, and framework integration patterns. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[killerapp](https://clawhub.ai/user/killerapp) <br>

### License/Terms of Use: <br>
Apache-2.0 <br>


## Use Case: <br>
Developers and engineers use this skill to turn natural language requirements into BAML project files for structured LLM outputs, multimodal extraction, classification, RAG, and agent workflows. It helps produce source files, tests, framework integration code, and generation commands for Python, TypeScript, Ruby, and Go targets. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated BAML project files and integration code may contain incorrect logic or unsafe changes. <br>
Mitigation: Review generated diffs before committing or deploying them. <br>
Risk: BAML generation can run local on_generate hooks. <br>
Mitigation: Inspect any on_generate hook before running baml-cli generate. <br>
Risk: External model providers may receive sensitive document, image, audio, or internal workflow data. <br>
Mitigation: Use trusted providers and MCP servers, and apply consent, redaction, and provider controls before processing sensitive data. <br>


## Reference(s): <br>
- [BAML Reference Guide for AI Agents](references/BAML-REFERENCE-SOURCE.md) <br>
- [Provider Configuration Reference](references/providers.md) <br>
- [BAML Types and Schemas Reference](references/types-and-schemas.md) <br>
- [Validation Patterns Reference](references/validation.md) <br>
- [BAML Pattern Library](references/patterns.md) <br>
- [MCP Interface and Query Strategy](references/mcp-interface.md) <br>
- [Python + BAML Reference](references/languages-python.md) <br>
- [TypeScript + BAML Reference](references/languages-typescript.md) <br>
- [LangGraph + BAML Integration Reference](references/frameworks-langgraph.md) <br>
- [BAML Documentation](https://docs.boundaryml.com) <br>
- [BAML Examples Repository](https://github.com/BoundaryML/baml-examples) <br>
- [BAML Releases](https://github.com/BoundaryML/baml/releases) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with BAML, Python, TypeScript, Ruby, Go, and shell code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include .baml source, tests, framework integration code, generated metadata, cost estimates, and validation steps.] <br>

## Skill Version(s): <br>
2.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
