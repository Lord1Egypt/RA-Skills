## Description:

Exa MCP integration for advanced search, research, and crawling.

This skill is ready for commercial/non-commercial use.

## Publisher:

[claireaicodes](https://clawhub.ai/user/claireaicodes)

### License/Terms of Use:

MIT

## Use Case:

Developers and agent builders use this skill to let OpenClaw agents perform Exa-powered web search, code context lookup, webpage crawling, company research, people search, and deep research tasks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Agents may send search terms, URLs, and research subjects to Exa.

Mitigation: Install only for agents that need external web research and review what kinds of queries those agents may submit.

Risk: EXA_API_KEY can be exposed if stored in workspace .env files or system-wide shell configuration.

Mitigation: Use OpenClaw scoped configuration or another secret manager for EXA_API_KEY, and avoid committing or broadly exporting the credential.

Risk: Exa search and research results may contain incomplete, stale, or misleading third-party content.

Mitigation: Have agents cite and verify important findings before relying on results for decisions or generated deliverables.

## Reference(s):

- [Exa MCP Documentation](https://exa.ai/docs/reference/exa-mcp)
- [Exa MCP Server](https://mcp.exa.ai/mcp)
- [Exa API Keys](https://dashboard.exa.ai/api-keys)
- [OpenClaw Skills Guide](https://docs.openclaw.ai/skills/)
- [ClawHub Skill Page](https://clawhub.ai/claireaicodes/skills/exa-tool)

## Skill Output:

**Output Type(s):** [Text, API Calls, Shell commands]

**Output Format:** [JSON responses with search results, crawled page content, research results, and error messages on stderr]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires EXA_API_KEY and sends agent-provided search terms, URLs, and research subjects to Exa.]

## Skill Version(s):

1.0.0 (source: package.json and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
