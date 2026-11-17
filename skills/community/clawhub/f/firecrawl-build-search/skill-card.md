## Description:

Integrate Firecrawl `/search` into product code and agent workflows. Use when an app needs discovery before extraction, when the feature starts with a query instead of a URL, or when the system should search the web and optionally hydrate result content.

This skill is ready for commercial/non-commercial use.

## Publisher:

[eohmig](https://clawhub.ai/user/eohmig)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to add Firecrawl query-based web discovery to products or agent workflows, especially when a workflow must find sources before scraping or extracting content.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search queries may be sent to Firecrawl when the skill is used for hosted web discovery.

Mitigation: Use this skill only in environments where sharing those queries with Firecrawl is acceptable, and avoid sending sensitive queries unless approved.

Risk: A Firecrawl API key is required for hosted requests.

Mitigation: Provide FIRECRAWL_API_KEY only through approved secret-management mechanisms and avoid hard-coding it in generated code or configuration.

## Reference(s):

- [Firecrawl homepage](https://www.firecrawl.dev)
- [Firecrawl skills repository](https://github.com/firecrawl/skills)
- [Firecrawl Node / TypeScript source of truth](https://docs.firecrawl.dev/agent-source-of-truth/node)
- [Firecrawl Python source of truth](https://docs.firecrawl.dev/agent-source-of-truth/python)
- [Firecrawl Rust source of truth](https://docs.firecrawl.dev/agent-source-of-truth/rust)
- [Firecrawl Java source of truth](https://docs.firecrawl.dev/agent-source-of-truth/java)
- [Firecrawl Elixir source of truth](https://docs.firecrawl.dev/agent-source-of-truth/elixir)
- [Firecrawl cURL / REST source of truth](https://docs.firecrawl.dev/agent-source-of-truth/curl)
- [ClawHub skill page](https://clawhub.ai/eohmig/skills/firecrawl-build-search)

## Skill Output:

**Output Type(s):** [guidance, markdown, code, shell commands, configuration]

**Output Format:** [Markdown guidance with implementation notes, code snippets, command examples, and configuration details.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May reference FIRECRAWL_API_KEY for hosted Firecrawl requests and optional FIRECRAWL_API_URL for self-hosted deployments.]

## Skill Version(s):

1.0.0 (source: release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
