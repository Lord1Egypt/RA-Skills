## Description:

Integrate Firecrawl `/interact` into product code for dynamic pages and browser actions after scraping.

This skill is ready for commercial/non-commercial use.

## Publisher:

[eohmig](https://clawhub.ai/user/eohmig)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to integrate Firecrawl browser interaction workflows when scraping requires clicks, form fills, pagination, filters, or authenticated multi-step page actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Interact workflows may send page content, form data, or authenticated-session-derived data to Firecrawl or a configured backend.

Mitigation: Use the narrowest workflow possible, avoid highly sensitive sites without approval, and prefer self-hosted or tightly scoped deployments where appropriate.

Risk: Persistent profiles can retain authenticated state across sessions.

Mitigation: Use persistent profiles only when authenticated state is required and review the workflow scope before deployment.

Risk: Open-ended browser automation may exceed the intended product workflow.

Mitigation: Keep action prompts or code specific to the product flow and evaluate a browser sandbox for fully open-ended automation.

## Reference(s):

- [Firecrawl Homepage](https://www.firecrawl.dev)
- [Firecrawl Node / TypeScript Source of Truth](https://docs.firecrawl.dev/agent-source-of-truth/node)
- [Firecrawl Python Source of Truth](https://docs.firecrawl.dev/agent-source-of-truth/python)
- [Firecrawl Rust Source of Truth](https://docs.firecrawl.dev/agent-source-of-truth/rust)
- [Firecrawl Java Source of Truth](https://docs.firecrawl.dev/agent-source-of-truth/java)
- [Firecrawl Elixir Source of Truth](https://docs.firecrawl.dev/agent-source-of-truth/elixir)
- [Firecrawl cURL / REST Source of Truth](https://docs.firecrawl.dev/agent-source-of-truth/curl)

## Skill Output:

**Output Type(s):** [Guidance, Code, Shell commands, Configuration]

**Output Format:** [Markdown guidance with code and command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May require FIRECRAWL_API_KEY and optionally FIRECRAWL_API_URL for hosted or self-hosted Firecrawl integrations.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
