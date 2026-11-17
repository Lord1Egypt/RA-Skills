## Description:

Generates a complete set of AI readiness files for any website from a single command.

This skill is ready for commercial/non-commercial use.

## Publisher:

[russwittmann](https://clawhub.ai/user/russwittmann)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, marketers, and site owners use this skill to research a website and generate AI-readiness files that help AI assistants, search systems, and RAG pipelines understand and represent the site.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad activation wording can cause the skill to run during loosely related AI crawler, llms.txt, RAG indexing, or AI-search requests.

Mitigation: Confirm the target domain and intended file generation task before execution, especially when the user is asking a general question rather than requesting generated files.

Risk: Unpinned npx installer and MCP usage can introduce supply-chain or hosted-service trust risk.

Mitigation: Prefer manual installation from reviewed files or pin and inspect npm packages before running installer commands; use the hosted MCP only with site data you are comfortable sending to that service.

Risk: The workflow creates many files in the workspace and produces content intended for deployment to a website root.

Mitigation: Run the skill in a controlled workspace and review generated files, URLs, policies, and crawler directives before deploying them publicly.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/russwittmann/skills/ai-readiness)
- [AI Readiness Documentation](https://ai.silverbackmarketing.com)
- [AI Readiness MCP Documentation](https://ai.silverbackmarketing.com/#mcp)
- [npm Package](https://www.npmjs.com/package/@silverbackmarketing/ai-readiness)
- [llmstxt.org](https://llmstxt.org/)
- [AI Readiness File Specifications](references/file-specs.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, XML, JSONL, Shell commands, Configuration, Guidance]

**Output Format:** [Workspace folder containing 18 website AI-readiness files plus a concise completion summary.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The generated set includes deployable web-root files, project documentation, and a JSONL file derived from rag-index.json.]

## Skill Version(s):

1.0.0 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
