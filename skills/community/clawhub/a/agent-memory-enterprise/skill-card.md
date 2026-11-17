## Description:

Enterprise-grade 5-layer agent memory system with routing, scoring, and multi-backend storage for production AI agents that need persistent memory with PostgreSQL, Redis, and ChromaDB support.

This skill is ready for commercial/non-commercial use.

## Publisher:

[laojun509](https://clawhub.ai/user/laojun509)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to add persistent, routed memory to production AI agents across conversation context, task state, user profiles, knowledge retrieval, and experience learning.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill persistently stores and reuses user, task, conversation, and document data.

Mitigation: Avoid indexing secrets or regulated data, define retention and deletion controls, and review stored memory policies before shared or enterprise deployment.

Risk: Shared deployments may expose memory across users or tenants without application controls.

Mitigation: Deploy behind application-level authentication and tenant isolation before enabling production or multi-user use.

Risk: Retrieved memories can carry stale, sensitive, or prompt-injection content into downstream LLM prompts.

Mitigation: Treat all retrieved memory as untrusted and validate, filter, or redact it before including it in an LLM prompt.

Risk: The skill depends on external Redis, PostgreSQL, and ChromaDB storage configuration.

Mitigation: Use approved storage services and access controls, and review configuration before installing in shared environments.

## Reference(s):

- [Agent Memory Pro - API Reference](artifact/references/api_reference.md)
- [Agent Memory Pro - Usage Examples](artifact/references/examples.md)
- [ClawHub Skill Page](https://clawhub.ai/laojun509/skills/agent-memory-enterprise)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with Python and shell code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces memory-system integration guidance, configuration examples, and code snippets for agent implementations.]

## Skill Version(s):

0.1.0 (source: server release metadata and pyproject.toml)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
